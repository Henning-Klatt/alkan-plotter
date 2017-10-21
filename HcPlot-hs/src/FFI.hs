{-# LANGUAGE ForeignFunctionInterface #-}

module FFI where

import HcPlot
import Foreign
import Foreign.C.Types
import Foreign.C.String

foreign export ccall createRandomMolecule_c :: CInt -> CInt -> IO CString
createRandomMolecule_c :: CInt -> CInt -> IO CString
createRandomMolecule_c len dep = newCString . show . createRandomMolecule (fromEnum len) $ (fromEnum dep)
