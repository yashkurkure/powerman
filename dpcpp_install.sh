export DPCPP_HOME=~/sycl_workspace
mkdir $DPCPP_HOME
cd $DPCPP_HOME

mkdir -p cmake-3.27 && wget -qO- "https://cmake.org/files/v3.27/cmake-3.27.0-linux-x86_64.tar.gz" | tar --strip-components=1 -xz -C cmake-3.27
~ $ export PATH=`pwd`/cmake-3.27/bin:$PATH

git clone https://github.com/intel/llvm -b sycl

python3 $DPCPP_HOME/llvm/buildbot/configure.py
python3 $DPCPP_HOME/llvm/buildbot/compile.py
