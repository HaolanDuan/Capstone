import os

MAXN = 1000000
VectorDefaultSize = 20
TOPNUM = 1

class iVector:
    def __init__(self):
        self.m_size = VectorDefaultSize
        self.m_data = [None] * VectorDefaultSize
        self.m_num = 0

    def free_mem(self):
        del self.m_data

    def push_back(self, d):
        if self.m_num == self.m_size:
            self.re_allocate(self.m_size * 2)
        self.m_data[self.m_num] = d
        self.m_num += 1

    def push_back(self, p, length):
        while self.m_num + length > self.m_size:
            self.re_allocate(self.m_size * 2)
        self.m_data[self.m_num:self.m_num+length] = p
        self.m_num += length

    def re_allocate(self, size):
        if size < self.m_num:
            return
        tmp = [None] * size
        tmp[:self.m_num] = self.m_data
        self.m_size = size
        del self.m_data
        self.m_data = tmp

    def Sort(self):
        if self.m_num < 20:
            for i in range(self.m_num-1):
                k = i
                for j in range(i+1, self.m_num):
                    if self.m_data[j] < self.m_data[k]:
                        k = j
                if k != i:
                    tmp = self.m_data[i]
                    self.m_data[i] = self.m_data[k]
                    self.m_data[k] = tmp
        else:
            self.m_data.sort()

    def unique(self):
        if self.m_num == 0:
            return
        self.Sort()
        j = 0
        for i in range(self.m_num):
            if self.m_data[i] != self.m_data[j]:
                j += 1
                if j != i:
                    self.m_data[j] = self.m_data[i]
        self.m_num = j + 1

    def BinarySearch(self, data):
        x = 0
        y = self.m_num - 1
        while x <= y:
            p = (x + y) // 2
            if self.m_data[p] == data:
                return p
            if self.m_data[p] < data:
                x = p + 1
            else:
                y = p - 1
        return -1

    def clean(self):
        self.m_num = 0

    def assign(self, t):
        self.m_num = t.m_num
        self.m_size = t.m_size
        del self.m_data
        self.m_data = t.m_data

    def remove(self, x):
        l = 0
        r = self.m_num
        while l < r:
            m = (l + r) // 2
            if self.m_data[m] == x:
                self.m_num -= 1
                if self.m_num > m:
                    self.m_data[m:self.m_num] = self.m_data[m+1:self.m_num+1]
                return True
            elif self.m_data[m] < x:
                l = m + 1
            else:
                r = m
        return False

    def sorted_insert(self, x):
        if self.m_num == 0:
            self.push_back(x)
            return
        if self.m_num == self.m_size:
            self.re_allocate(self.m_size * 2)
        l = 0
        r = self.m_num
        while l < r:
            m = (l + r) // 2
            if self.m_data[m] < x:
                l = m + 1
            else:
                r = m
        if l < self.m_num and self.m_data[l] == x:
            pass
        else:
            if self.m_num > l:
                self.m_data[l+1:self.m_num+1] = self.m_data[l:self.m_num]
            self.m_num += 1
            self.m_data[l] = x

    def remove_unsorted(self, x):
        for m in range(self.m_num):
            if self.m_data[m] == x:
                self.m_num -= 1
                if self.m_num > m:
                    self.m_data[m:self.m_num] = self.m_data[m+1:self.m_num+1]
                return True
        return False

    def __getitem__(self, i):
        return self.m_data[i]

class iMap:
    def __init__(self):
        self.m_data = None
        self.m_num = 0
        self.cur = 0
        self.occur = iVector()

    def free_mem(self):
        del self.m_data
        self.occur.free_mem()

    def initialize(self, n):
        self.occur.re_allocate(n)
        self.occur.clean()
        self.m_num = n
        if self.m_data is not None:
            del self.m_data
        self.m_data = [None] * self.m_num
        self.cur = 0

    def clean(self):
        for i in range(self.occur.m_num):
            self.m_data[self.occur[i]] = None
        self.occur.clean()
        self.cur = 0

    def init_keys(self, n):
        self.occur.re_allocate(n)
        self.occur.clean()
        self.m_num = n
        if self.m_data is not None:
            del self.m_data
        self.m_data = [0] * self.m_num
        for i in range(self.m_num):
            self.occur.push_back(i)
            self.cur += 1

    def reset_zero_values(self):
        self.m_data = [0] * self.m_num

    def reset_one_values(self):
        self.m_data = [1] * self.m_num

    def get(self, p):
        return self.m_data[p]

    def __getitem__(self, p):
        return self.m_data[p]

    def erase(self, p):
        self.m_data[p] = None
        self.cur -= 1

    def notexist(self, p):
        return self.m_data[p] is None

    def exist(self, p):
        return self.m_data[p] is not None

    def insert(self, p, d):
        if self.m_data[p] is None:
            self.occur.push_back(p)
            self.cur += 1
        self.m_data[p] = d

    def inc(self, p, x=1):
        self.m_data[p] += x

    def dec(self, p):
        self.m_data[p] -= 1

class PendingQueue:
    def __init__(self, n):
        self.queue = iVector()
        self.pos = iMap()
        self.point = 0

    def clean(self):
        self.queue.clean()
        self.point = 0
        self.pos.clean()

    def push_back(self, x):
        self.pos.insert(x, self.queue.m_num)
        self.queue.push_back(x)

    def pop(self):
        while self.point < self.queue.m_num:
            if self.pos.get(self.queue[self.point]) == self.point:
                self.point += 1
                return self.queue[self.point-1]
            self.point += 1
        return -1

def ltrim(s):
    return s.lstrip()

def rtrim(s):
    return s.rstrip()

def trim(s):
    return s.strip()

def __n_variable(t, n):
    return t + str(n)

def ___debug(t, *args):
    os = ""
    for i, arg in enumerate(args):
        os += __n_variable(t, i) + str(arg) + " "
    return os

def ___debug(t, t0, os):
    os += __n_variable(t, 0) + str(t0) + " "

def ___debug(t, t0, t1, os):
    os += __n_variable(t, 0) + str(t0) + " " + __n_variable(t, 1) + str(t1) + " "

def ___debug(t, t0, t1, t2, os):
    os += __n_variable(t, 0) + str(t0) + " " + __n_variable(t, 1) + str(t1) + " " + __n_variable(t, 2) + str(t2) + " "

def ___debug(t, t0, t1, t2, t3, os):
    os += __n_variable(t, 0) + str(t0) + " " + __n_variable(t, 1) + str(t1) + " " + __n_variable(t, 2) + str(t2) + " " + __n_variable(t, 3) + str(t3) + " "

def ___debug(t, t0, t1, t2, t3, t4, os):
    os += __n_variable(t, 0) + str(t0) + " " + __n_variable(t, 1) + str(t1) + " " + __n_variable(t, 2) + str(t2) + " " + __n_variable(t, 3) + str(t3) + " " + __n_variable(t, 4) + str(t4) + " "

def ___debug(t, t0, os):
    os += __n_variable(t, 0)
    for i in range(len(t0)):
        os += str(t0[i]) + " "
    return os

def ___debug(t, t0, os):
    os += __n_variable(t, 0)
    for i in range(len(t0)):
        os += str(t0[i]) + " "
    return os

def ___debug(t, t0, os):
    os += __n_variable(t, 0)
    for i in range(len(t0)):
        os += str(t0[i].F) + "," + str(t0[i].S) + " "
    return os

def RUN_TIME(*args):
    t = rdtsc()
    args
    t = rdtsc() - t
    print(" : ", t / TIMES_PER_SEC, "s")

def TRACE(*args):
    print(___debug(*args))

def IF_TRACE(args):
    args

def TRACE_LINE(*args):
    print(___debug(*args), end="")
    print("                    ", end="")

def TRACE_SKIP(a, *args):
    static_c = -1
    static_c += 1
    if static_c % a == 0:
        TRACE(*args)

def TRACE_LINE_SKIP(a, *args):
    static_c = -1
    static_c += 1
    if static_c % a == 0:
        TRACE_LINE(*args)

def TRACE_LINE_END(*args):
    print()

def TRACE_LOG(*args):
    print(___debug(*args))

def ASSERT(v):
    if not v:
        print("ASSERT FAIL @ ", __FILE__, ":", __LINE__)
        exit(1)

def INFO(*args):
    print(___debug(*args))

def ASSERTT(v, *args):
    if not v:
        print("ASSERT FAIL @ ", __FILE__, ":", __LINE__)
        INFO(*args)
        exit(1)

def toStr(t):
    return str(t)

class Counter:
    cnt = [0] * 1000
    def __init__(self, id=0):
        self.myid = id
        Counter.cnt[id] += 1

    def add(self, x):
        Counter.cnt[self.myid] += x

    def __del__(self):
        pass

    @staticmethod
    def show():
        for i in range(1000):
            if Counter.cnt[i] > 0:
                INFO("Counter", i, Counter.cnt[i])

def rdtsc():
    return 0

class Timer:
    timeUsed = []
    timeUsedDesc = []
    def __init__(self, id, desc="", showOnDestroy=False):
        self.id = id
        while len(Timer.timeUsed) <= id:
            Timer.timeUsed.append(0)
            Timer.timeUsedDesc.append("")
        Timer.timeUsedDesc[id] = desc
        self.startTime = 0
        self.showOnDestroy = showOnDestroy

    @staticmethod
    def used(id):
        return Timer.timeUsed[id] / TIMES_PER_SEC

    def __del__(self):
        duration = (chrono.steady_clock.now() - self.startTime).count()
        if self.showOnDestroy:
            print("time spend on ", Timer.timeUsedDesc[self.id], ":", duration / TIMES_PER_SEC, "s")
        Timer.timeUsed[self.id] += duration

    @staticmethod
    def show(debug=False):
        if debug:
            TRACE("### Timer")
        else:
            INFO("### Timer")
        for i in range(len(Timer.timeUsed)):
            if Timer.timeUsed[i] > 0:
                s = str(Timer.timeUsed[i] / TIMES_PER_SEC)
                if len(s) < 15:
                    s = " " + s
                t = "{:4d} {} {}".format(i, s, Timer.timeUsedDesc[i])
                if debug:
                    TRACE(t)
                else:
                    INFO(t)

    @staticmethod
    def reset(id):
        Timer.timeUsed[id] = 0

    @staticmethod
    def clearAll():
        Timer.timeUsed.clear()
        Timer.timeUsedDesc.clear()

def combine_args(argc, argv):
    args = []
    for i in range(argc):
        args.append(argv[i])
    return args

def to_str(t):
    return str(t)

def file_exists_test(name):
    return os.path.isfile(name)

def replace(str, from_str, to_str):
    return str.replace(from_str, to_str)

def get_proc_memory():
    return 0

Green = "\033[0;32m"
Reset = "\033[0m"
Red = "\033[0;31m"

def get_current_time_str():
    rawtime = time.time()
    timeinfo = time.localtime(rawtime)
    buffer = time.strftime("%Y-%m-%d %H:%M:%S", timeinfo)
    return buffer

def program_start(argc, argv):
    print(Green, "--------------start------------", get_current_time_str(), Reset)
    combine = ""
    for i in range(1, argc):
        combine += argv[i]
        combine += " "
    print(Green, "args:", combine, Reset)

def program_stop():
    print(Red, "--------------stop------------", get_current_time_str(), Reset)
    print()
    print()
    print()

def ASSERTMSG(condition, message):
    if not condition:
        print("ASSERT FAIL @ ", __FILE__, ":", __LINE__, message)
        exit(1)

