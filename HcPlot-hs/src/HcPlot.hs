module HcPlot where

import HcPlot.Names
import HcPlot.Molecule
import System.Random
import Data.List

{-| How long can a sidechain be at xth C molecule |-}
maxSideChainLen :: Int -> [Int]
maxSideChainLen x = undefined
    where half = concat . map (\a -> [a,a])
