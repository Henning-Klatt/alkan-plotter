module HcPlot where

import HcPlot.Names
import HcPlot.Molecule

{-| How long can a sidechain be at xth C molecule |-}
maxSideChainLen :: Int -> [Int]
maxSideChainLen x = if length half * 2 == x
                       then half ++ reverse half
                       else 0 : half ++ reverse half
    where maxValue = (fst $ divMod x 2) - 1
          half = [0..maxValue]
