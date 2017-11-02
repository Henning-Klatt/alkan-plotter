module HcPlot.Names
    ( getNames
    , nameToLength
    , nameToLength'
    , stripSuffix
    , stripNamePrefix
    , prefixToLength
    , lengthToPrefix
    ) where

import Data.List

getNames :: Int -> String
getNames x = names !! (x-1)

{-| Get the length of a name with suffix |-}
nameToLength :: String -> Int
nameToLength = nameToLength' . stripSuffix

{-| Get the length of a name without suffix |-}
nameToLength' :: String -> Int
nameToLength' name =
    case elemIndex name names of
        Just x  -> (x + 1)
        Nothing -> -1

{-| Convert a prefix to the corresponding number |-}
prefixToLength :: String -> Int
prefixToLength name =
    case elemIndex name prefixes of
        Just x  -> (x + 1)
        Nothing -> -1

{-| Convert a number to the corresponing Prefix |-}
lengthToPrefix :: Int -> String
lengthToPrefix = (!!) prefixes . subtract 1

{-| Strip a prefix from a given string |-}
stripNamePrefix :: String -> Maybe String
stripNamePrefix str = flip (!!) 0 . filter (/= Nothing) . zipWith stripPrefix prefixes $ (repeat str)

{-| Strips a suffix (either "yl" or "an") from a name |-}
stripSuffix :: String -> String
stripSuffix name = take (len - 2) name
    where len = length name

prefixes :: [String]
prefixes = [ "hen"
           , "di"
           , "tri"
           , "tetra"
           , "penta"
           , "hexa"
           , "hepta"
           , "octa"
           , "nona"
           , "deca"
           , "undeca"
           , "dodeca"
           , "trideca"
           , "tetradeca"
           ]


names :: [String]
names = [ "meth"
        , "eth"
        , "prop"
        , "but"
        , "pent"
        , "hex"
        , "hept"
        , "oct"
        , "non"
        , "dec"
        , "undec"
        , "dodec"
        , "tridec"
        , "tetradec"
        , "pentadec"
        , "hexadec"
        , "heptadec"
        , "octadec"
        , "nonadec"
        , "icos"
        , "henicos"
        , "docos"
        , "tricos"
        , "tetracos"
        , "pentacos"
        , "hexacos"
        , "heptacos"
        , "octacos"
        , "nonacos"
        , "triacont"
        , "hentriacont"
        , "dotriacont"
        , "tritriacont"
        , "tetratriacont"
        , "pentatriacont"
        , "hexatriacont"
        , "heptatriacont"
        , "octatriacont"
        , "nonatriacont"
        , "tetracont"
        , "hentetracont"
        , "dotetracont"
        , "tritetracont"
        , "tetratetracont"
        , "pentatetracont"
        , "hexatetracont"
        , "heptatetracont"
        , "octatetracont"
        , "nonatetracont"
        , "pentacont"
        , "henpentacont"
        , "dopentacont"
        , "tripentacont"
        , "tetrapentacont"
        , "pentapentacont"
        , "hexapentacont"
        , "heptapentacont"
        , "octapentacont"
        , "nonapentacont"
        , "hexacont"
        , "henhexacont"
        , "dohexacont"
        , "trihexacont"
        , "tetrahexacont"
        , "pentahexacont"
        , "hexahexacont"
        , "heptahexacont"
        , "octahexacont"
        , "nonahexacont"
        , "heptacont"
        , "henheptacont"
        , "doheptacont"
        , "triheptacont"
        , "tetraheptacont"
        , "pentaheptacont"
        , "hexaheptacont"
        , "heptaheptacont"
        , "octaheptacont"
        , "nonaheptacont"
        , "octacont"
        , "henoctacont"
        , "dooctacont"
        , "trioctacont"
        , "tetraoctacont"
        , "pentaoctacont"
        , "hexaoctacont"
        , "heptaoctacont"
        , "octaoctacont"
        , "nonaoctacont"
        , "nonacont"
        , "hennonacont"
        , "dononacont"
        , "trinonacont"
        , "tetranonacont"
        , "pentanonacont"
        , "hexanonacont"
        , "heptanonacont"
        , "octanonacont"
        , "nonanonacont"
        , "hect"
        , "henihect"
        , "dohect"
        , "trihect"
        , "tetrahect"
        , "pentahect"
        , "hexahect"
        , "heptahect"
        , "octahect"
        , "nonahect"
        , "decahect"
        , "undecahect"
        , "dodecahect"
        , "tridecahect"
        , "tetradecahect"
        , "pentadecahect"
        , "hexadecahect"
        , "heptadecahect"
        , "octadecahect"
        , "nonadecahect"
        , "icosahect"
        ]
