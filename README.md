# Dithering-with-Pascal-Triangle
In this article, I present a cellular automaton (CA) which evolve according to a set of rules derived from a well known combinatorial structure, the Pascal's Triangle. With only 2 neighbour cells, this probabilistic cellular automaton (PCA) produces point sampling commonly observed in high-quality digital dithering and halftoning techniques. 

Feel free to play and share your discoveries :) 

Related article to come... 

Note: this version already implement int8 vs uint8, or just to fix the Threshold at 127 or to 
play with threshol modulation and negative values < maybe > the halftone result is uint8   

Note: it's not completly discrete since it sample from an random uniform distribution U(0, 1), but.. ;) 

python3.9 PCADithering.py IMAGE_PNG/Lion.png