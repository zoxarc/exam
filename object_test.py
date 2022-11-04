from objects.template import Event, Handle


def test(handle: Handle):
    handle()


if __name__ == '__main__':
    test_event = Event()
    test_event += test

    args = Handle()
    test_event(args)
    print(args.value)
