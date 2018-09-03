from time import sleep

from django_celery_beat.schedulers import DatabaseScheduler


class AutoUpdateScheduler(DatabaseScheduler):
    def all_as_schedule(self):
        print(self.Model.objects.all())
        return super(AutoUpdateScheduler, self).all_as_schedule()

    def tick(self, *args, **kwargs):
        if self.schedule_changed():
            print('Resetting heap')
            self.sync()
            self._heap = None
            sleep(1)
            new_schedule = self.all_as_schedule()

            to_add = [key for key in new_schedule.keys() if key not in self.schedule]
            to_remove = [key for key in self.schedule.keys() if key not in new_schedule]
            if new_schedule:
                for key in to_add:
                    self.schedule[key] = new_schedule[key]
                for key in to_remove:
                    del self.schedule[key]

        super(AutoUpdateScheduler, self).tick(*args, **kwargs)

    @property
    def schedule(self):
        if not self._initial_read and not self._schedule:
            self._initial_read = True
            self._schedule = self.all_as_schedule()
        return self._schedule
