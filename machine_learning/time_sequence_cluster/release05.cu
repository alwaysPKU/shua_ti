#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <memory.h>
#include <fstream>
#include <sstream>

#include <vector>
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>
#include <thrust/transform.h>
#include <thrust/sequence.h>
#include <thrust/copy.h>
#include <thrust/fill.h>
#include <thrust/replace.h>
#include <thrust/functional.h>
#include <thrust/extrema.h>
#include <algorithm>

#include "cublas_v2.h"
#include "cuda_runtime.h"



#define Threshold 0.5

#define HASFN 1
#define HASLABEL 0

// #define NEEDNORMALIZATION 1
// #define MAXDIM 256
#define MAXPERBATCH 1000000
#define MAXSIZE 2000000
#define alloc_size 20000
#define IDX2C(i, j, ld) ((j)*(ld) +(i))
// #define MAXOUTPUTNUM 100000000
// #define unsigned long long LL
#define CHECK_CUBLAS_ERROR(state) if(CUBLAS_STATUS_SUCCESS != state) \
printf("ERROR state %d in file %s at line %d.\n", state, __FILE__, __LINE__);


typedef  struct featsMat
{
     float* mat  = 0;
     int length = 0;
     int  dim = 0;
    
}featM;

struct saxpy_functor
{
    const int a;

    saxpy_functor(int _a) : a(_a) {}

    __host__ __device__
        thrust::pair    <float, int  > operator()(const float& x, const int& y) const { 
            return ( thrust::pair    <float,int> (x,y) );
        }
};

struct is_true
{
    const float threshold;

    is_true(float _threshold) : threshold(_threshold) {}

  __host__ __device__
  bool operator()( const thrust::pair    <float,int> &x )
  {
    // return (x.first>=Threshold)&&(x.first <0.9999);
    return x.first>= threshold;
  }
};


void normalizegpu( float* A, int l1,int dim) {
//not parallel
    float *dev_mat1 = 0, *norm = 0;
    CHECK_CUBLAS_ERROR(cudaMalloc((void**)&dev_mat1, dim*sizeof(float)));
    norm = (float*)malloc(dim*sizeof(float));

    cublasHandle_t matAddHandle;
    cublasCreate(&matAddHandle);
    for ( int i=0;i<l1;i++){
            CHECK_CUBLAS_ERROR(cublasSetVector(dim, sizeof(float), A+i*dim, 1, dev_mat1, 1));
            CHECK_CUBLAS_ERROR(cublasSnrm2(matAddHandle,dim, dev_mat1, 1, norm)); 
            *norm=1/(*norm);
            CHECK_CUBLAS_ERROR(cublasSscal(matAddHandle,dim, norm,dev_mat1,1)); 
            CHECK_CUBLAS_ERROR(cublasGetVector( dim, sizeof(float),dev_mat1 , 1 , A+i*dim, 1));
    }

    CHECK_CUBLAS_ERROR(cublasDestroy(matAddHandle));
    CHECK_CUBLAS_ERROR(cudaFree(dev_mat1));
}



extern "C" void calcthreshold( float* A, float* B,int* paras,float threshold, int* index1,int* index2,float* scores) {
    //paras[int l1,int l2,int dim,int lvalue,int cnt,int gpuno  
//    cudaSetDevice(paras[5]);
    clock_t starttime,endtime;
    starttime=clock();
    int l1=paras[0],l2=paras[1],dim=paras[2],lvalue=paras[3],cnt=paras[4],cntlimit=paras[5],cardno=paras[6];
    cudaSetDevice(cardno);
    endtime=clock();
//    std::cout<<"set GPU"<<(double)(endtime-starttime)/CLOCKS_PER_SEC<<std::endl;


    float alpha = 1.0f;
    float beta = 0.0f;
    //FILE *stream; 
    //stream = fopen(fn, "w+");
    float *dev_mat1 = 0, *dev_mat2 = 0, *dev_y = 0;//, *seq = 0;//, *ttest = 0 ;//, *A_tmp, *B_tmp;
    thrust::pair    <float,int> *d_vector= 0, *true_vect = 0;
    int offset = 0,sum=0;
    int ceili=ceil((float)l2/alloc_size);
    int ceilj=ceil((float)l1/alloc_size);
    clock_t t1 = clock();
    int alloc_sizeA=min(l1,alloc_size);
    int alloc_sizeB=min(l2,alloc_size);
//    cudaDeviceSetLimit(cudaLimitMallocHeapSize, ((uint64_t)4*alloc_size*alloc_size)); 
    CHECK_CUBLAS_ERROR(cudaMalloc((void**)&dev_mat1, (alloc_sizeA*dim)*sizeof(float)));
    CHECK_CUBLAS_ERROR(cudaMalloc((void**)&dev_mat2, (alloc_sizeB*dim)*sizeof(float)));
    CHECK_CUBLAS_ERROR(cudaMalloc((void**)&dev_y, (alloc_sizeA*alloc_sizeB)*sizeof(float)));
    CHECK_CUBLAS_ERROR(cudaMalloc((void**)&d_vector, (alloc_sizeA*alloc_sizeB)*sizeof(thrust::pair    <float,int>)));
    CHECK_CUBLAS_ERROR(cudaMalloc((void**)&true_vect, (alloc_sizeA*alloc_sizeB)*sizeof(thrust::pair    <float,int>)));
    

    clock_t t2 = clock();
  //  printf("malloc : %lf\n",(double)(t2-t1)/CLOCKS_PER_SEC);

    cublasHandle_t matAddHandle;
    cublasCreate(&matAddHandle);
    thrust::host_vector< thrust::pair    <float,int> > h_vector(MAXPERBATCH);
//    printf("l1=%d, l2=%d\n",l1,l2);   


    for ( int i=0;i<ceili;i++){//ceili
        int lb=min(l2-alloc_size*i,alloc_size);
        CHECK_CUBLAS_ERROR(cublasSetMatrix(lb, dim, sizeof(float), B+(uint64_t)alloc_size*i*dim, lb, dev_mat2, lb));
        for ( int j=0;j<ceilj;j++){//ceilj
             clock_t t22 = clock();
            int la=min(l1-alloc_size*j,alloc_size);
           // printf("i=%d , j= %d , la=%d, lb=%d v=%f\n",i,j,la,lb,*A);
            CHECK_CUBLAS_ERROR(cublasSetMatrix(la, dim, sizeof(float), A+(uint64_t)alloc_size*j*dim, la, dev_mat1, la));
           
            clock_t t3 = clock();
//             printf("set value: %lf\n",(double)(t3-t22)/CLOCKS_PER_SEC);
          
             clock_t t4 = clock();
            CHECK_CUBLAS_ERROR(cublasSgemm(matAddHandle, CUBLAS_OP_T, CUBLAS_OP_N, lb, la,dim,
                &alpha, dev_mat2, dim, dev_mat1, dim , &beta, dev_y,lb));
            
             clock_t t5 = clock();
//             printf("calculation : %lf  %d %d \n",(double)(t5-t3)/CLOCKS_PER_SEC, la, lb);

            thrust::device_ptr<float> iter( dev_y ); 
            thrust::device_ptr<thrust::pair <float,int> > dv( d_vector ); 
            thrust::device_ptr<thrust::pair <float,int> > tv( true_vect ); 

//            printf("now transform %d %d \n",i ,j );
            clock_t t6 = clock();
            thrust::transform(iter, iter+la*lb,  thrust::make_counting_iterator(0), dv, saxpy_functor(1));// i*ceilj +j may be dealt with later
//            printf("12321321313\n");
            offset = thrust::copy_if(dv, dv+la*lb, tv, is_true(threshold)) - tv ;
            sum+=offset;
//            printf("offset = %d\n",offset);
            int batches=(offset-1)/MAXPERBATCH+1;
            int pleft=0,pright=min(offset,MAXPERBATCH);
            while(batches--)
            {//   printf("%d %d %d\n",pleft,pright,batches);
                thrust::copy(tv+pleft,tv+pright,h_vector.begin());  
                for(int it=0;it<pright-pleft;it++)
                {
                    index1[paras[4]]=lvalue+j*alloc_size+h_vector[it].second/lb;
                    index2[paras[4]]=i*alloc_size+h_vector[it].second%lb;
                    scores[paras[4]]=h_vector[it].first;
                    paras[4]+=1;
                    if(paras[4]>=cntlimit)
                        return;
                    //fprintf(stream, "%d %d %f\n",  lvalue+j*alloc_size+h_vector[it].second/lb, i*alloc_size+h_vector[it].second%lb, h_vector[it].first);
                    
                }
                pleft=pright;
                pright+=min(MAXPERBATCH,offset-pleft);
                
            }
//            cudaDeviceSynchronize();
            
        }
    }
    clock_t t3=clock();
//    printf("malloc : %lf\n",(double)(t3-t2)/CLOCKS_PER_SEC);
    //printf("l1=%d, l2=%d, dim=%d\n",l1,l2,dim);
    //printf("cardno:%d sum:%d\n",cardno,sum);
    //printf("%d %d %d %f\n",cardno,ceili,ceilj,*A);


    CHECK_CUBLAS_ERROR(cublasDestroy(matAddHandle));
    CHECK_CUBLAS_ERROR(cudaFree(dev_y));
    CHECK_CUBLAS_ERROR(cudaFree(dev_mat1));
    CHECK_CUBLAS_ERROR(cudaFree(dev_mat2));
    CHECK_CUBLAS_ERROR(cudaFree(d_vector));
    CHECK_CUBLAS_ERROR(cudaFree(true_vect));
    //fclose(stream);

}

void gen_init_matrix(float* dst, int rows, int cols, float min_val = 0, float max_val = 1) {
    if (NULL == dst)
        exit(-1);
    for (int r = 0; r < rows*cols; ++r) {
        dst[r] = (1.0f * (rand( )) / RAND_MAX) *(max_val - min_val) + min_val;
    }
}

void trans_mat(float* mat, int rows, int cols ) {
    float* tmp = (float*)(malloc)(rows*cols*sizeof(float));
    memcpy((void*)tmp, (void*)mat, rows*cols*sizeof(float));
    int count = 0;
    for (int i = 0; i < cols; ++i) {
        for (int j = 0; j < rows; ++j) {
            mat[count++] = tmp[j*cols + i];
        }
    }
    free(tmp);
}

void cpu_test(int rows, int cols, int dim, float* A, float* x, float* y, float alpha, float beta) {
    float* dst = (float*)malloc(rows*cols*(sizeof(float)));
    for (int i = 0; i < rows; ++i) {
//        float sum = 0.0f;
        for (int j = 0; j < cols; ++j){
            float sum = 0.0f;
            for (int k =0; k<dim;++k){
                sum += A[i*dim + k] * x[j*dim+k] * alpha;
            }
//        dst[i] = sum /*+ beta * y[i]*/;
//            printf("%2.6f\t", sum);
        }
    }
}

// void test( ) {
//     cudaSetDevice(2);
//     int rows = 500000, cols = 500000, dim= 256;
//     float *mat1 = 0, *mat2 = 0, *mat3 = 0;
//     mat1 = (float*)malloc(rows*dim*(sizeof(float)));
//     mat2 = (float*)malloc(cols*dim*sizeof(float));
//     mat3 = (float*)malloc(alloc_size*alloc_size*sizeof(float));
//     gen_init_matrix(mat1, rows, dim, 0, 1);
//     gen_init_matrix(mat2, cols, dim , 0, 1);
//     gen_init_matrix(mat3, alloc_size, alloc_size, 0, 1);

// printf("cpu : %lf\n",(double)(t2-t1)/CLOCKS_PER_SEC);

//    trans_mat(mat1, rows, cols);
//    printf("mat1\n");
//    for (int i = 0; i < rows; ++i) {
//        for (int j = 0; j < dim; ++j)
//            printf("%f\t", mat1[i*dim + j]);
//        printf("\n");
//    }
//    printf("mat2\n");
//    for (int i = 0; i < cols; ++i) {
//        for (int j = 0; j < dim; ++j)
//          printf("%f\t", mat2[i*dim + j]);
//        printf("\n");
//    }
//    printf("\n");
//    printf("%f %f %f %d %d %d\n",*mat3,*mat1,*mat2,rows,cols,dim);    
    // clock_t t3 = clock();
    // printf("gpu : %lf\n",(double)(t3-t2)/CLOCKS_PER_SEC);

// }

// void readFeaturesCPU(char* fin, featM &ret)
// {
//     ret.mat = (float*)malloc(MAXSIZE*MAXDIM*(sizeof(float)));
//     std::ifstream featfile(fin);
//     if(!featfile.is_open()) {
//         std::cout << "can't open " << fin << std::endl;
//         exit(-1);
//     }
//     int linecnt = 0 , cnt = 0 , iDim = 0 ;
//     for (std::string strLine; std::getline(featfile, strLine); linecnt++)
//     {
//         std::istringstream iss(strLine);
//         if (HASFN)
//         {
//             std::string strFn;
//             iss >> strFn;
//         }
//         if (HASLABEL)
//         {
//             int tmp=0;
//             iss >> tmp;
//         }
//         iDim = 0;
//         while(iss >> ret.mat[cnt])
//             iDim+=1,cnt+=1;

   
//     }
//     ret.length = linecnt;
//     ret.dim = iDim;
//     printf("cnt == %d, linecnt*iDim = %d \n",cnt,linecnt * iDim);
//     assert(cnt == linecnt * iDim);


// }


int getDimCnt(char* buff)
{
  int i=0,dim=1 - HASFN - HASLABEL ;
  while(buff[i]!='\n')
  {
    if (buff[i]==' ' && buff[i-1]!=' ')
    {
        dim+=1;
    }
    i+=1;

  }
  return dim;

}
/*void readFeaturesGPU(char* fin, featM &ret)
{
    clock_t t1 = clock();
    
    std::ifstream inFile(fin, std::ios::binary | std::ios::in);
    inFile.seekg(0, std::ios::end);
    uint64_t nFileLen = inFile.tellg();
    std::vector<char> buf(nFileLen + 1ULL);
    std::cout << "Allocated " << nFileLen << " bytes" << std::endl;
    
    inFile.seekg(0, std::ios::beg);
    inFile.read(buf.data(), nFileLen);
    int dim = getDimCnt(buf.data());
    buf[nFileLen] = 0;
    std::cout << "Loaded " << nFileLen << " bytes" << std::endl;

    std::vector<uint64_t> lineBegins;
    lineBegins.push_back(0);
#pragma omp parallel
    {
#pragma omp for
    for (uint64_t i = 0; i < buf.size(); ++i)
    {
        if (buf[i] == '\n')
        {
#pragma omp critical
            lineBegins.push_back(i + 1);
            buf[i] = 0;
        }
    }
    }
    uint64_t nLineCnt = lineBegins.size() - 1;
    lineBegins.push_back(buf.size());
    std::cout << "Find " << nLineCnt << " lines" << std::endl;
    
    std::sort(lineBegins.begin(), lineBegins.end());
    std::cout << "Line begin positions sorted" << std::endl;


    
    printf("dimension of feature is %d\n",dim);

    ret.mat = (float*)malloc(nLineCnt*dim*(sizeof(float)));
    ret.length = nLineCnt;
    ret.dim = dim;
    float *features = ret.mat;
    // std::vector< std::array<float, 128> > features;
    // features.resize(nLineCnt);
    int stepsize=2000000*256/dim;
    for (uint64_t i = 0 ; i < nLineCnt;)
    {
        std::vector<uint64_t> begs;
        uint64_t iNext = std::min(nLineCnt, i + stepsize);
        char *pBase = buf.data() + lineBegins[i];
        // float *pOut = (float*)features[i].data();
        float *pOut = features + i*dim;
        std::cout << "Find index" << std::endl;
#pragma omp parallel for
        for (int j = i; j < iNext; ++j)
        {   
            // std::cout <<j << std::endl;
            char *pLine  = buf.data() + lineBegins[j];
            uint64_t jPos=0;
            if (HASFN)
            {               
                
                for (jPos = 0; pLine[jPos] != ' '; jPos++)
                    ;   
                if (HASLABEL)
                {
                    ++jPos;
                }
                for (; pLine[jPos] != ' '; jPos++)
                    ;
            }
                                                                



             // printf("%s",pLine[jPos + 1]);
            // for (int cc=jPos + 1; pLine[cc] != ' '; cc++)
            //  printf("%c",pLine[cc]);
            // printf("\n");
#pragma omp critical
            if (HASFN)
                begs.push_back(pLine + jPos + 1 - pBase);
            else
                begs.push_back(pLine  - pBase);

        }

        std::sort(begs.begin(), begs.end());
        std::cout << "Copy to GPU " << i << std::endl;

        
        StringsToFloatVectors(
                pBase,
                buf.data() + lineBegins[iNext] - pBase,
                begs,
                pOut,
                dim
                );
        i = iNext;

        
    }
    buf.clear();
    buf.shrink_to_fit();
    clock_t t2 = clock();
    printf("done reading! time:%f\n",(float)(t2-t1)/CLOCKS_PER_SEC);
    // for(int i=0;i<128;i++)
    //     printf("%f ",ret.mat[i]);
    // ret.mat = features;
    


}*/

void printMatrix( float* x, int rows , int dim)
{

    printf("the matrix is :\n");
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < dim; ++j)
           printf("%f ", x[i*dim + j]);
       printf("\n");
   }
}


int main(int argc, char** argv ) {

   
    return 0;
}
