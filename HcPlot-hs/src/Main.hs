module Main where

import HcPlot
import System.Environment

main :: IO ()
main = do
    args <- getArgs
    putStrLn . show . createRandomMolecule (read $ args !! 0) $ (read $ args !! 1)
