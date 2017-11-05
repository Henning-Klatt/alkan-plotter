module Main where

import HcPlot.Molecule
import System.Environment

main :: IO ()
main = do
    args <- getArgs
    if args !! 0 == "r"
       then undefined
       else if args !! 0 == "n"
               then putStrLn . show $ nameToMolecule (args !! 1)
               else putStrLn ""
