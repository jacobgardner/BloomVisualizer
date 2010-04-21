sources = $(wildcard *.cpp)
objects = $(sources:%.cpp=%.o)
deps = $(sources:%.cpp=%.d)
CFLAGS += -g
CXXFLAGS += -g -I/usr/include/boost-1_37 -I/usr/include/python2.4
LDLIBS += -lboost_python-gcc41-mt-1_37 -lpython2.4


CPPFLAGS = -DSHOW_NETWORK 
override CPPFLAGS += -Isexp 

all: $(objects) visualizer

%.d: %.cpp
	@set -e; rm -f $@; \
	(dirname $< | tr '\n' '/'; $(CXX) -MM $(CPPFLAGS) $<) > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$

.PHONY: clean all subdirs

clean:
	rm -f $(objects) $(deps) visualizer
	$(MAKE) -C ../visualizer/sexp clean

visualizer: $(objects) ../visualizer/parser.o ../visualizer/structures.o
	$(CXX) $(CXXFLAGS) $(LOADLIBES) -fPIC -c *.cpp
	$(CXX) $(CXXFLAGS) $(LOADLIBES) $(LDLIBS) -shared -Wl,-soname,libparsermodule.so.1  ../visualizer/sexp/libclient*.o -o libparsermodule.so $^


../visualizer/sexp/sexp.a ../visualzer/sexp/libclient_sexp.a ../visualizer/parser.o ../visualizer/structures.o:
	$(MAKE) -C ../visualizer/sexp
#$(dir $@) $(notdir $@)

-include $(deps)
