export DPCPP_HOME=~/sycl_workspace
mkdir $DPCPP_HOME
cd $DPCPP_HOME

git clone https://github.com/intel/llvm -b sycl

python3 $DPCPP_HOME/llvm/buildbot/configure.py
python3 $DPCPP_HOME/llvm/buildbot/compile.py
