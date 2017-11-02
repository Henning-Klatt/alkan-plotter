module HcPlot where

import Data.List.Split
import HcPlot.Names

data Molecule = Int Molecule Molecule Molecule Molecule
              | C Molecule Molecule Molecule
              | H
              deriving (Eq)

data Name = Number Int
          | Name String

instance Show Molecule where
    show (Int a b c d) = "[" ++ show a ++ "," ++ show b ++ "," ++ show c ++ "," ++ show d ++ "]"
    show (C a b c)     = "[" ++ show a ++ "," ++ show b ++ "," ++ show c ++ "]"
    show H             = "\"" ++ "h" ++ "\""

{-| How long can a sidechain be at xth C molecule |-}
maxSideChainLen :: Int -> [Int]
maxSideChainLen x = if length half * 2 == x
                       then half ++ reverse half
                       else 0 : half ++ reverse half
    where maxValue = (fst $ divMod x 2) - 1
          half = [0..maxValue]

{-| Create a semi-random chain with len C-atoms and max lev sidechains |-}
createRandomChain :: Int -> Int -> Molecule
createRandomChain = undefined

{-| Create a random molecule with len main-chain C-atoms |-}
createRandomMolecule :: Int -> Int -> Molecule
createRandomMolecule len dep = liftMolecule $ createRandomChain len dep

{-| Make a chain longer |-}
liftMolecule :: Molecule -> Molecule
liftMolecule (C a b c) = Int H a b c
liftMolecule H         = H
liftMolecule _         = undefined

{-| Create a molecule from a name |-}
nameToMolecule :: String -> Molecule
nameToMolecule = liftMolecule . nameToChain

{-| Create a chain from a name |-}
nameToChain :: String -> Molecule
nameToChain str = constructMolecule $ mainLength
    where (sideChains, mainLength) = let s               = splitString str
                                         (loc, len)      = splitAt (length s - 1) s
                                         lenNameTuple    = tupleFoo loc
                                         toNumbers (x,y) = ((read ("["++x++"]"):: [Int]),
                                                            case stripNamePrefix y of
                                                                Just i -> i
                                                                Nothing -> "")
                                        -- Parse the string to a list of side chains + locations
                                        -- and the length of the mainchain
                                      in (map toNumbers lenNameTuple, nameToLength . concat  $ len)

          tupleFoo :: [a] -> [(a,a)]
          tupleFoo []       = []
          tupleFoo (_:[])   = []
          tupleFoo (x:y:ys) = (x,y) : tupleFoo ys
          findInLocations len = case filter (\(x,_) -> elem len x) $ sideChains of
                                    [(_,xs),(_,ys)] -> (nameToChain xs, nameToChain ys)
                                    [(_,xs)]        -> (nameToChain xs, H)
                                    _               -> (H, H)
          constructMolecule len
              | len == 0  = H
              | otherwise = (uncurry C) (findInLocations len) (constructMolecule (len-1))


-- XXX: THIS IS UGLY
splitString str =  filter (/= "") . concat $ (zipWith ($) (cycle [splitOn "-", (:[])]) (splitOneOf "()" str))
