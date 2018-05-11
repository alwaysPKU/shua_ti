export CUDA_HOME=/usr/local/cuda
export LD_LIBRARY_PATH=${CUDA_HOME}/lib64
PATH=${CUDA_HOME}/bin:${PATH}
export PATH

nvcc -arch=sm_61  -rdc=true --compiler-options  -fPIC -shared -o libthreshold.so release05.cu  -I/usr/local/cuda/include -L/usr/local/cuda/lib64 -lcudart -lcublas -Xcompiler -fopenmp


#nvcc -arch=sm_61  -rdc=true --compiler-options  -fPIC -shared -o libtopranker.so ranker3.cu -I/usr/local/cuda/include -L/usr/local/cuda/lib64 -lcudart -lcublas -Xcompiler -fopenmp

#nvcc -arch=sm_61  -std=c++11 -rdc=true -o release04 release04.cu  string2float.cu -lcublas -lcublas_device -lcudadevrt  -Xcompiler -fopenmp
