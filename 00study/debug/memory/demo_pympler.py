import resource
import sys
import types

from pympler import asizeof, tracker
from pympler.tracker import SummaryTracker
from pympler.web import start_in_background, start_profiler


def demo_tracker():
    tracker = SummaryTracker()

    # ... some code you want to investigate ...

    tracker.print_diff()


def demo_ClassTracker():
    class Employee:
        pass

    class Factory:
        pass

    def create_factory():
        factory = Factory()
        factory.name = "Assembly Line Unlimited"
        factory.employees = []
        return factory

    def populate_factory(factory):
        for x in range(1000):
            worker = Employee()
            worker.assigned = factory.name
            factory.employees.append(worker)

    factory = create_factory()

    from pympler.classtracker import ClassTracker
    tracker = ClassTracker()
    tracker.track_object(factory)
    tracker.track_class(Employee)
    tracker.create_snapshot()

    populate_factory(factory)

    tracker.create_snapshot()
    tracker.stats.print_summary()

    tracker.stats.dump_stats('profile.dat')
    from pympler.classtracker_stats import ConsoleStats

    stats = ConsoleStats()
    stats.load_stats('profile.dat')
    stats.sort_stats('size').print_stats(limit=10, clsname='Node')

    from pympler.classtracker_stats import HtmlStats
    HtmlStats(tracker=tracker).create_html('profile.html')


memlist = []


# class MemoryCallback(keras.callbacks.Callback):
class MemoryCallback():
    def on_epoch_end(self, epoch, log={}):
        x = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        web_browser_debug = True
        print(x)

        if x > 40000:
            if web_browser_debug:
                if epoch == 0:
                    start_in_background()
                    tr = tracker.SummaryTracker()
                    tr.print_diff()
            else:
                global memlist
                all_objects = muppy.get_objects(include_frames=True)
                # print(len(all_objects))
                sum1 = summary.summarize(all_objects)
                memlist.append(sum1)
                summary.print_(sum1)
                if len(memlist) > 1:
                    # compare with last - prints the difference per epoch
                    diff = summary.get_diff(memlist[-2], memlist[-1])
                    summary.print_(diff)
                my_types = muppy.filter(all_objects, Type=types.ClassType)

                for t in my_types:
                    print(t)


if __name__ == '__main__':
    # demo_tracker()

    obj = [1, 2, (3, 4), 'text']

    print("sys.getsizeof", sys.getsizeof(obj))
    print("asizeof", asizeof.asizeof(obj))
    print("basicsize", asizeof.basicsize(obj))
    print("itemsize", asizeof.itemsize(obj))

    print(asizeof.asized(obj, detail=1).format())

    # demo_ClassTracker()

    print("*" * 30)
    from pympler import muppy

    all_objects = muppy.get_objects()
    # print(all_objects)
    print(len(all_objects))

    my_types = muppy.filter(all_objects, Type=type)
    print(len(my_types))
    # for t in my_types:
    #     print(t)

    from pympler import summary

    sum1 = summary.summarize(all_objects)
    summary.print_(sum1)

    print("*" * 40)
    sum2 = summary.summarize(muppy.get_objects())
    diff = summary.get_diff(sum1, sum2)
    summary.print_(diff)

    start_profiler()
