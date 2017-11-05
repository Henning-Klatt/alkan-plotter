module HcPlot.Molecule
    ( nameToMolecule
    , locationsToString
    , stringToLocations
    , Molecule ()
    , SideChainInformation
    ) where

import Data.List.Split
import HcPlot.Names

data Molecule = Int Molecule Molecule Molecule Molecule
              | C Molecule Molecule Molecule
              | H
              deriving (Eq)

type SideChainInformation = [([Int], Either String Int)]

instance Show Molecule where
    show (Int a b c d) = "[" ++ show a ++ "," ++ show b ++ "," ++ show c ++ "," ++ show d ++ "]"
    show (C a b c)     = "[" ++ show a ++ "," ++ show b ++ "," ++ show c ++ "]"
    show H             = "\"" ++ "h" ++ "\""

showLocations :: SideChainInformation -> String
showLocations [] = ""
showLocations (x:xs) =
    case snd x of
        Right y -> numbers ++ "-" ++ prefix ++ lengthToName y ++ "yl" ++ "-"
        Left y  -> numbers ++ "-" ++ "(" ++ y ++ ")" ++ showLocations xs ++ "-"
     where
         prefix = lengthToPrefix . length . fst $ x
         numbers = tail . init . show $ fst x

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
    where (sideChains, mainLength) = stringToLocations str
          constructMolecule len
              | len == 0  = H
              | otherwise = (uncurry C) (findInLocations sideChains len) (constructMolecule (len-1))

locationsToString :: (SideChainInformation, Int) -> String
locationsToString (loc, len) = showLocations loc ++ lengthToName len ++ "an"

{-| Create normal chain of length x |-}
createLinearChain :: Int -> Molecule
createLinearChain 0 = H
createLinearChain x = C H H (createLinearChain (x-1))

{-| Find the sidechains of a given position |-}
findInLocations :: SideChainInformation -> Int -> (Molecule, Molecule)
findInLocations [] _ = (H,H)
findInLocations (x:xs) pos
    | pos == 0           = (H,H)
    | elem pos . fst $ x = case snd x of
                                Right y -> (createLinearChain y, fst . findInLocations xs $ pos)
                                Left y  -> (nameToChain y, fst . findInLocations xs $ pos)
    | otherwise          = findInLocations xs (pos-1)

{-| Get the SideChainInformation and the lenght of the main chain of a given name |-}
stringToLocations :: String -> (SideChainInformation, Int)
stringToLocations str = (map toNumbers lenNameTuple, nameToLength . concat  $ len)
    where
        s               = splitString str
        (loc, len)      = splitAt (length s - 1) s
        lenNameTuple    = tupleFoo loc
        toNumbers (x,y) = (read ("["++x++"]") :: [Int],
                           case stripNamePrefix y of
                               Just i -> Right (nameToLength i)
                               Nothing -> Left y)
        tupleFoo :: [a] -> [(a,a)]
        tupleFoo []       = []
        tupleFoo (_:[])   = []
        tupleFoo (x:y:ys) = (x,y) : tupleFoo ys


-- XXX: THIS IS UGLY
splitString :: String -> [String]
splitString str =  filter (/= "") . concat $ (zipWith ($) (cycle [splitOn "-", (:[])]) (splitOneOf "()" str))
