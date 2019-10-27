#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Python.h>

#include "MLX90640_I2C_Driver.h"
#include "MLX90640_API.h"


static PyObject * wrapper_init(PyObject * self, PyObject * args)
{
  PyObject * ret;
  PyObject * subList;
  paramsMLX90640 *mlx90640_params_handle;
  uint16_t* memory;

  memory = MLX90640_I2CInit();
  
  mlx90640_params_handle = (paramsMLX90640 *)malloc(sizeof(paramsMLX90640));
  
  ret = PyInt_FromLong((long int)mlx90640_params_handle);
  ret = PyList_New(6);
  // subList = PyList_New(10);
  // PyList_SetItem(subList, 0, PyInt_FromLong(memory[0]));
  // PyList_SetItem(subList, 1, PyInt_FromLong(memory[1]));
  // PyList_SetItem(subList, 2, PyInt_FromLong(memory[2]));
  // PyList_SetItem(subList, 3, PyInt_FromLong(memory[3]));
  // PyList_SetItem(subList, 4, PyInt_FromLong(memory[4]));
  PyList_SetItem(ret, 0, PyInt_FromLong((long int)mlx90640_params_handle));
  // PyList_SetItem(ret, 1, subList);
  PyList_SetItem(ret, 1, PyInt_FromLong((long int)memory));
  PyList_SetItem(ret, 2, PyInt_FromLong((long int)memory[0]));
  PyList_SetItem(ret, 3, PyInt_FromLong((long int)memory[1]));
  PyList_SetItem(ret, 4, PyInt_FromLong((long int)memory[2]));
  PyList_SetItem(ret, 5, PyInt_FromLong((long int)memory[3]));
  return ret;

  ret = PyInt_FromLong((long int)mlx90640_params_handle);
  return ret;
}

static PyObject * wrapper_close(PyObject * self, PyObject * args)
{
    PyObject * ret;
    long int handle = 0;

    //parse arguments
    if (!PyArg_ParseTuple(args, "l", &handle)) {
        return NULL;
    }

    free((paramsMLX90640 *)handle);

    ret = ret = PyInt_FromLong(0);

    return ret;
}

static PyObject * wrapper_readMem(PyObject * self, PyObject * args)
{
    PyObject * ret;
    long int memAddr = 0;
    long int dataLen = 0;
    uint16_t wordData;
    int status;
    uint16_t *eeData;
    int i;

    //parse arguments
    if (!PyArg_ParseTuple(args, "ll", &memAddr, &dataLen)) {
        return NULL;
    }

    if(dataLen > 1)
    {
      eeData = (uint16_t *)malloc(832 * sizeof(uint16_t));
      ret = PyList_New(dataLen);
      // status = MLX90640_I2CRead(0x33, memAddr, (uint16_t)dataLen, eeData);
      status = MLX90640_DumpEE(0x33, eeData);
      // eeData[821] =  (uint16_t)0;
      // ret = PyInt_FromLong(eeData[0]);
      for(i = 0; i < dataLen; i++)
      {
        PyList_SetItem(ret, i, PyInt_FromLong((long int)eeData[i]));
      }
      return ret;      
    }
    else
    {
      status = MLX90640_I2CRead(0x33, memAddr, (uint16_t)dataLen, &wordData);
      ret = PyInt_FromLong(wordData);
      return ret; 
    }
}

static PyObject * wrapper_setKsTa(PyObject * self, PyObject * args)
{
    PyObject * ret;
    float inputVal;
    long int handle = 0;

    //parse arguments
    if (!PyArg_ParseTuple(args, "lf", &handle, &inputVal)) {
        return NULL;
    }

    ((paramsMLX90640*)handle)->KsTa = inputVal;

    ret = ret = PyInt_FromLong(0);

    return ret;
}

static PyObject * wrapper_getKsTa(PyObject * self, PyObject * args)
{
    PyObject * ret;
    long int handle = 0;

    //parse arguments
    if (!PyArg_ParseTuple(args, "l", &handle)) {
        return NULL;
    }

    ret = PyFloat_FromDouble((double)((paramsMLX90640*)handle)->KsTa);

    return ret;
}

static PyObject * wrapper_DumpEE(PyObject * self, PyObject * args)
{
  PyObject * ret;
  int status, i;
  unsigned char slaveAddr;
  PyObject * inputList;
  PyObject * outputList;
  Py_ssize_t len;
  uint16_t *eeData = (uint16_t *)malloc(832 * sizeof(uint16_t));
  memset(eeData, 0xFF, 832 * sizeof(uint16_t));
  //parse arguments
  if (!PyArg_ParseTuple(args, "bO", &slaveAddr, &inputList)) {
    return NULL;
  }

  status = MLX90640_DumpEE(slaveAddr, eeData);
  len = PyList_Size(inputList);
  outputList = PyList_New(len);
  //return PyInt_FromLong(eeData[1]);
  if(1/*status == 0 && len == 832*/)
  {
    for(i = 0; i < len; i++)
    {
      status = PyList_SetItem(inputList, i, PyInt_FromLong(0x23));
      status = PyList_SetItem(inputList, i, PyInt_FromLong((unsigned long int)0x0000FFFF & (unsigned long int)eeData[i]));
      status = PyList_SetItem(outputList, i, PyInt_FromLong((unsigned long int)0x0000FFFF & (unsigned long int)eeData[i]));
      if(status != 0)
        break;
    }
  }
  //0x00AE, 0x499A, 0x0000, 0x2061, 0x0005
  // PyList_SetItem(inputList, 0, PyInt_FromLong(0x00AE));
  // PyList_SetItem(inputList, 1, PyInt_FromLong(0x499A));
  // PyList_SetItem(inputList, 2, PyInt_FromLong(0x0000));
  // PyList_SetItem(inputList, 3, PyInt_FromLong(0x2061));
  // PyList_SetItem(inputList, 4, PyInt_FromLong(0x0005));
  // ret = PyInt_FromLong(status/*0xFFFF & eeData[0]*/);
  ret = outputList;
  free(eeData);
  return ret;
}

static PyObject * wrapper_ExtractParameters(PyObject * self, PyObject * args)
{
  PyObject * ret;
  int status, i;
  long int handleMlxParams = 0;
  PyObject * inputList;
  PyObject * listItem;
  Py_ssize_t len;
  uint16_t *eeData = (uint16_t *)malloc(832 * sizeof(uint16_t));
  
  paramsMLX90640 *MlxParamsBackup = (paramsMLX90640 *)malloc(sizeof(paramsMLX90640));
  memcpy(MlxParamsBackup, (paramsMLX90640 *)handleMlxParams, sizeof(paramsMLX90640));
  //parse arguments
  if (!PyArg_ParseTuple(args, "Ol", &inputList, &handleMlxParams)) {
    return NULL;
  }

  len = PyList_Size(inputList);

  // load EE Data from input list
  if(len == 832)
  {
    for(i = 0; i < len; i++)
    {
      listItem = PyList_GetItem(inputList, i);
      status = PyInt_Check(listItem);
      if(status != 1)
      {
        // in check type function 0 is NOK, thus convert to usual -1 as NOK
        status = -1;
        break;
      }
      else
      {
        eeData[i] = PyInt_AsLong(listItem);
      }
    }
  }

  status = MLX90640_ExtractParameters(eeData, (paramsMLX90640 *)handleMlxParams);
  // on extract failure, recover from backup
  if(status != 0)
  {
    memcpy((paramsMLX90640 *)handleMlxParams, MlxParamsBackup, sizeof(paramsMLX90640));
  }

  ret = PyInt_FromLong(status);
  free(eeData);
  free(MlxParamsBackup);
  return ret;
}

static PyMethodDef MathMethods[] = {
  { "init",        wrapper_init,               METH_VARARGS, "init function." },
  { "dumpEE",      wrapper_DumpEE,             METH_VARARGS, "init function." },
  // { "extract",     wrapper_ExtractParameters,  METH_VARARGS, "init function." },
  // { "init",        wrapper_GetFrameData,       METH_VARARGS, "init function." },
  // { "init",        wrapper_GetTa,              METH_VARARGS, "init function." },
  // { "init",        wrapper_CalculateTo,        METH_VARARGS, "init function." },
  // { "init",        wrapper_GetImage,           METH_VARARGS, "init function." },
  // { "init",        wrapper_SetResolution,      METH_VARARGS, "init function." },
  // { "init",        wrapper_GetCurResolution,   METH_VARARGS, "init function." },
  // { "init",        wrapper_SetRefreshRate,     METH_VARARGS, "init function." },
  // { "init",        wrapper_GetRefreshRate,     METH_VARARGS, "init function." },
  // { "init",        wrapper_GetSubPageNumber,   METH_VARARGS, "init function." },
  // { "init",        wrapper_GetCurMode,         METH_VARARGS, "init function." },
  // { "init",        wrapper_SetInterleavedMode, METH_VARARGS, "init function." },
  // { "init",        wrapper_SetChessMode,       METH_VARARGS, "init function." },
  { "readMem",       wrapper_readMem,            METH_VARARGS, "init function." },
  { "close",       wrapper_close,              METH_VARARGS, "init function." },
  { "setKsTa",     wrapper_setKsTa,            METH_VARARGS, "init function." },
  { "getKsTa",     wrapper_getKsTa,            METH_VARARGS, "init function." },
  { NULL, NULL, 0, NULL }
};

DL_EXPORT(void) initmlx(void)
{
  Py_InitModule("mlx", MathMethods);
}
