git submodule init
git submodule update
cd MUSE
python unsupervised.py --src_emb ../models/voynich.vec --tgt_emb ../models/secretaSecretorum.vec --n_refinement 5 --emb_dim 100 --dis_most_frequent 100 --dico_build S2T --cuda false
