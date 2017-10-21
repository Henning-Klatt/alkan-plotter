module HcPlot where

import HcPlot.Names
import Test.QuickCheck

data Molecule = Int Molecule Molecule Molecule Molecule
              | C Molecule Molecule Molecule
              | H
              deriving (Eq)

instance Show Molecule where
    show (Int a b c d) = "[" ++ show a ++ "," ++ show b ++ "," ++ show c ++ "," ++ show d ++ "]"
    show (C a b c)     = "[" ++ show a ++ "," ++ show b ++ "," ++ show c ++ "]"
    show H             = "\"" ++ "h" ++ "\""

{-| How long can a sidechain be at xth C molecule |-}
maxSideChainLen :: Int -> [Int]
maxSideChainLen x = if length half * 2 == x
                       then half ++ reverse half
                       else 0 : half ++ reverse half
    where max = (fst $ divMod x 2) - 1
          half = [0..max]

-- FIXME: Should do no side chains with dep = 0 and not dep = 1
{-| Create a random chain with len C-atoms and max lev sidechains |-}
createRandomChain :: Int -> Int -> Molecule
createRandomChain len dep = go (maxSideChainLen len) len dep
    where go _ _ 0 = H
          go _ 0 _ = H
          go (x:xs) len dep = C (createRandomChain x (dep-1))
                                (createRandomChain x (dep-1))
                                (go xs (len-1) dep)

{-| Create a random molecule with len main-chain C-atoms |-}
createRandomMolecule :: Int -> Int -> Molecule
createRandomMolecule len dep = apply $ createRandomChain len dep
    where apply (C a b c) = Int H a b c
          apply H         = H
