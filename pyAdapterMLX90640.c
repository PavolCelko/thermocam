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

  MLX90640_I2CInit();
  
  mlx90640_params_handle = (paramsMLX90640 *)malloc(sizeof(paramsMLX90640));
  
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

static PyObject * wrapper_getSomeParams(PyObject * self, PyObject * args)
{
    PyObject * ret;
    long int handle = 0;
    PyObject * outList = PyList_New(38);
    //parse arguments
    if (!PyArg_ParseTuple(args, "l", &handle)) {
        return NULL;
    }

    PyList_SetItem(outList, 0, PyInt_FromLong(((paramsMLX90640*)handle)->kVdd));
    PyList_SetItem(outList, 1, PyInt_FromLong(((paramsMLX90640*)handle)->vdd25));
    PyList_SetItem(outList, 2, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->KvPTAT));
    PyList_SetItem(outList, 3, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->KtPTAT));
    PyList_SetItem(outList, 4, PyInt_FromLong(((paramsMLX90640*)handle)->vPTAT25));
    PyList_SetItem(outList, 5, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->alphaPTAT));
    PyList_SetItem(outList, 6, PyInt_FromLong(((paramsMLX90640*)handle)->gainEE));
    PyList_SetItem(outList, 7, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->tgc));
    PyList_SetItem(outList, 8, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->cpKv));
    PyList_SetItem(outList, 9, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->cpKta));
    PyList_SetItem(outList, 10, PyInt_FromLong(((paramsMLX90640*)handle)->resolutionEE));
    PyList_SetItem(outList, 11, PyInt_FromLong(((paramsMLX90640*)handle)->calibrationModeEE));
    PyList_SetItem(outList, 12, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->KsTa));
    PyList_SetItem(outList, 13, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->ksTo[0]));
    PyList_SetItem(outList, 14, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->ksTo[1]));
    PyList_SetItem(outList, 15, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->ksTo[2]));
    PyList_SetItem(outList, 16, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->ksTo[3]));
    PyList_SetItem(outList, 17, PyInt_FromLong(((paramsMLX90640*)handle)->ct[0]));
    PyList_SetItem(outList, 18, PyInt_FromLong(((paramsMLX90640*)handle)->ct[1]));
    PyList_SetItem(outList, 19, PyInt_FromLong(((paramsMLX90640*)handle)->ct[2]));
    PyList_SetItem(outList, 20, PyInt_FromLong(((paramsMLX90640*)handle)->ct[3]));
    PyList_SetItem(outList, 21, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->cpAlpha[0]));
    PyList_SetItem(outList, 22, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->cpAlpha[1]));
    PyList_SetItem(outList, 23, PyInt_FromLong(((paramsMLX90640*)handle)->cpOffset[0]));
    PyList_SetItem(outList, 24, PyInt_FromLong(((paramsMLX90640*)handle)->cpOffset[1]));
    PyList_SetItem(outList, 25, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->ilChessC[0]));
    PyList_SetItem(outList, 26, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->ilChessC[1]));
    PyList_SetItem(outList, 27, PyFloat_FromDouble((double)((paramsMLX90640*)handle)->ilChessC[2]));
    PyList_SetItem(outList, 28, PyInt_FromLong(((paramsMLX90640*)handle)->brokenPixels[0]));
    PyList_SetItem(outList, 29, PyInt_FromLong(((paramsMLX90640*)handle)->brokenPixels[1]));
    PyList_SetItem(outList, 30, PyInt_FromLong(((paramsMLX90640*)handle)->brokenPixels[2]));
    PyList_SetItem(outList, 31, PyInt_FromLong(((paramsMLX90640*)handle)->brokenPixels[3]));
    PyList_SetItem(outList, 32, PyInt_FromLong(((paramsMLX90640*)handle)->brokenPixels[4]));
    PyList_SetItem(outList, 33, PyInt_FromLong(((paramsMLX90640*)handle)->outlierPixels[0]));
    PyList_SetItem(outList, 34, PyInt_FromLong(((paramsMLX90640*)handle)->outlierPixels[1]));
    PyList_SetItem(outList, 35, PyInt_FromLong(((paramsMLX90640*)handle)->outlierPixels[2]));
    PyList_SetItem(outList, 36, PyInt_FromLong(((paramsMLX90640*)handle)->outlierPixels[3]));
    PyList_SetItem(outList, 37, PyInt_FromLong(((paramsMLX90640*)handle)->outlierPixels[4]));
    
    ret = outList;

    return ret;
}

static PyObject * wrapper_DumpEE(PyObject * self, PyObject * args)
{
  PyObject * ret;
  int status, i;
  unsigned char slaveAddr;
  PyObject * inputList;
  Py_ssize_t len;
  uint16_t *eeData = (uint16_t *)malloc(832 * sizeof(uint16_t));
  memset(eeData, 0xFF, 832 * sizeof(uint16_t));

  //parse arguments
  if (!PyArg_ParseTuple(args, "bO", &slaveAddr, &inputList)) {
    return NULL;
  }

  status = MLX90640_DumpEE(slaveAddr, eeData);
  len = PyList_Size(inputList);
  if(status == 0 && len == 832)
  {
    for(i = 0; i < len; i++)
    {
      status = PyList_SetItem(inputList, i, PyInt_FromLong(0x23));
      status = PyList_SetItem(inputList, i, PyInt_FromLong((unsigned long int)0x0000FFFF & (unsigned long int)eeData[i]));
      if(status != 0)
        break;
    }
  }
  ret = PyInt_FromLong(status);
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
  paramsMLX90640 *MlxParamsBackup;

  //parse arguments
  if (!PyArg_ParseTuple(args, "Ol", &inputList, &handleMlxParams)) {
    return NULL;
  }

  MlxParamsBackup = (paramsMLX90640 *)malloc(sizeof(paramsMLX90640));
  if(MlxParamsBackup == 0)
    return PyInt_FromLong(-1);
  memcpy(MlxParamsBackup, (paramsMLX90640 *)handleMlxParams, sizeof(paramsMLX90640));

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

static PyObject * wrapper_GetFrameData(PyObject * self, PyObject * args)
{
  PyObject * ret;
  int status, i;
  unsigned char slaveAddr;
  PyObject * inputList;
  Py_ssize_t len;
  uint16_t *frameData = (uint16_t *)malloc(834 * sizeof(uint16_t));
  if(frameData == 0)
    return PyInt_FromLong(-1);
  // memset(frameData, 0xFF, 834 * sizeof(uint16_t));

  //parse arguments
  if (!PyArg_ParseTuple(args, "bO", &slaveAddr, &inputList)) {
    return NULL;
  }

  status = MLX90640_GetFrameData(slaveAddr, frameData);
  len = PyList_Size(inputList);
  if(status == 0 && len == 834)
  {
    for(i = 0; i < len; i++)
    {
      status = PyList_SetItem(inputList, i, PyInt_FromLong(frameData[i]));
      if(status != 0)
        break;
    }
  }
  ret = PyInt_FromLong(status);
  free(frameData);
  return ret;
}

static PyObject * wrapper_GetTa(PyObject * self, PyObject * args)
{
  PyObject * ret;
  float TaVal;
  long int handleMlxParams = 0;
  int i;
  PyObject * inputList;
  PyObject * listItem;
  Py_ssize_t len;
  uint16_t *frameData;
  
  //parse arguments
  if (!PyArg_ParseTuple(args, "Ol", &inputList, &handleMlxParams)) {
    return NULL;
  }

  frameData = (uint16_t *)malloc(834 * sizeof(uint16_t));
  if(frameData == 0)
    return PyInt_FromLong(-1);
  len = PyList_Size(inputList);
  for(i = 0; i < len; i++)
  {
    listItem = PyList_GetItem(inputList, i);
    frameData[i] = PyInt_AsLong(listItem);
  }

  TaVal = MLX90640_GetTa(frameData, (paramsMLX90640 *)handleMlxParams);

  ret = PyFloat_FromDouble(TaVal);
  free(frameData);
  return ret;
}

static PyObject * wrapper_CalculateTo(PyObject * self, PyObject * args)
{
  PyObject * ret;
  float TaVal;
  int i;
  PyObject * inputList;
  PyObject * outputList;
  PyObject * listItem;
  Py_ssize_t lenInputList;
  Py_ssize_t lenOutputList;
  uint16_t *frameData;
  long int handleMlxParams = 0;
  float emissivity;
  float tr;
  float *result;
  int status = -1;

  //parse arguments
  if (!PyArg_ParseTuple(args, "OlffO", &inputList, &handleMlxParams, &emissivity, &tr, &outputList)) {
    return NULL;
  }

  lenInputList = PyList_Size(inputList);
  lenOutputList = PyList_Size(outputList);
  frameData = (uint16_t *)malloc(lenInputList * sizeof(uint16_t));
  result = (float *)malloc(lenOutputList * sizeof(float));
  if(frameData == 0 || result == 0)
    status = -1;
  else
  {
    for(i = 0; i < lenInputList; i++)
    {
      listItem = PyList_GetItem(inputList, i);
      frameData[i] = PyInt_AsLong(listItem);
    }
    for(i = 0; i < lenOutputList; i++)
    {
      listItem = PyList_GetItem(outputList, i);
      result[i] = PyFloat_AsDouble(listItem);
    }

    MLX90640_CalculateTo(frameData, (paramsMLX90640 *)handleMlxParams, emissivity, tr, result);

    for(i = 0; i < lenOutputList; i++)
    {
      status = PyList_SetItem(outputList, i, PyFloat_FromDouble(result[i]));
      if(status != 0)
        break;
    }
  }

  free(frameData);
  free(result);
  return PyInt_FromLong(status);
}

static PyObject * wrapper_GetSubPageNumber(PyObject * self, PyObject * args)
{
  Py_ssize_t lenInputList;
  int i, subpage;
  PyObject * listItem;
  PyObject * inputList;
  uint16_t * frameData;
  
  //parse arguments
  if (!PyArg_ParseTuple(args, "O", &inputList)) {
    return NULL;
  }

  lenInputList = PyList_Size(inputList);
  frameData = (uint16_t *)malloc(lenInputList * sizeof(uint16_t));
  if(frameData == 0)
    subpage = -1;
  else
  {
    for(i = 0; i < lenInputList; i++)
    {
      listItem = PyList_GetItem(inputList, i);
      frameData[i] = PyInt_AsLong(listItem);
    }
    subpage = MLX90640_GetSubPageNumber(frameData);
  }

  return PyInt_FromLong(subpage);
}
    
static PyMethodDef MathMethods[] = {
  { "init",        wrapper_init,               METH_VARARGS, "init function." },
  { "dumpEE",      wrapper_DumpEE,             METH_VARARGS, "init function." },
  { "extract",     wrapper_ExtractParameters,  METH_VARARGS, "init function." },
  { "getFrame",    wrapper_GetFrameData,       METH_VARARGS, "init function." },
  { "getTa",       wrapper_GetTa,              METH_VARARGS, "init function." },
  { "calcT0",      wrapper_CalculateTo,        METH_VARARGS, "init function." },
  // { "init",        wrapper_GetImage,           METH_VARARGS, "init function." },
  // { "init",        wrapper_SetResolution,      METH_VARARGS, "init function." },
  // { "init",        wrapper_GetCurResolution,   METH_VARARGS, "init function." },
  // { "init",        wrapper_SetRefreshRate,     METH_VARARGS, "init function." },
  // { "init",        wrapper_GetRefreshRate,     METH_VARARGS, "init function." },
  { "getSubPageNumber",        wrapper_GetSubPageNumber,   METH_VARARGS, "init function." },
  // { "init",        wrapper_GetCurMode,         METH_VARARGS, "init function." },
  // { "init",        wrapper_SetInterleavedMode, METH_VARARGS, "init function." },
  // { "init",        wrapper_SetChessMode,       METH_VARARGS, "init function." },
  // { "readMem",       wrapper_readMem,            METH_VARARGS, "init function." },
  { "close",       wrapper_close,              METH_VARARGS, "init function." },
  { "setKsTa",     wrapper_setKsTa,            METH_VARARGS, "init function." },
  { "getKsTa",     wrapper_getKsTa,            METH_VARARGS, "init function." },
  { "getSomeParams",     wrapper_getSomeParams,            METH_VARARGS, "init function." },
  { NULL, NULL, 0, NULL }
};

DL_EXPORT(void) initmlx(void)
{
  Py_InitModule("mlx", MathMethods);
}
