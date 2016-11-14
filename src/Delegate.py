from inspect import isclass


class Delegate(object):
    is_class = False

    def __init__(self, funcorclass):
        self.post_execute = []
        self.pre_execute = []
        self.call_with = []
        self.basefunc = funcorclass
        if isclass(self.basefunc):
            self.is_class = True
            setattr(self.basefunc, 'callwith', self.callwith)
            setattr(self.basefunc, 'callback', self.callback)
            setattr(self.basefunc, 'callbefore', self.callbefore)

    def __getitem__(self, item):
        return item

    def __getattr__(self, item):
        if self.is_class:
            return self.basefunc
        return item

    def __iadd__(self, func):
        if callable(func):
            self.__isub__(func)
            self.post_execute.append(func)
        return self

    # When using callbefore, make sure you return the new object.
    def callbefore(self, func):
        if callable(func):
            self.__isub__(func)
            self.pre_execute.append(func)
        return func

    def callwith(self, func):
        if callable(func):
            self.__isub__(func)
            self.call_with.append(func)
        return func

    def callback(self, func):
        if callable(func):
            self.__isub__(func)
            self.post_execute.append(func)
        return func

    def post_execute(self, func):
        self.callback(func)

    # Make sure that pre_execute always returns the object.
    def pre_execute(self, func):
        self.callbefore(func)

    def __isub__(self, func):
        try:
            self.post_execute.remove(func)
        except ValueError:
            pass
        return self

    def __call__(self, *args, **kwargs):
        for func in self.pre_execute:
            _args = func(*args, **kwargs)
            if _args is not None: args = [_args]

        result = self.basefunc(*args, **kwargs)

        for func in self.call_with:
            newresult = func(*args, **kwargs)
            result = result if newresult is None else newresult

        for func in self.post_execute:
            newresult = func(result)
            result = result if newresult is None else newresult
        return result
