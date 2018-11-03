# Voynich neighbors
# Graphing of the 'self' mappings of the Voynich data and Secreta Secretorum, 
# looking at the types of word clusters
# May 30, 2018; Claire

library(igraph)

x <- read.table(file="VoySelf.txt", as.is=TRUE, header=TRUE)
x$Dist2 <- x$Dist * 1000 # For using the distance as an edge scale, but I didn't implement it.

q <- as.data.frame(x[1:2000,])  # closest 2000 matches
y <- as.data.frame(x[1:1000,])  # closest 1000 matches
g<-graph.data.frame(y, directed=FALSE)   # closest 1000 matches
f<-graph.data.frame(q, directed=FALSE)   # closest 2000 matches
plot(g)   # closest 1000 matches

# This stuff is sensitive to the number of pairs plotted; two few and you miss
# associations; too many and random stuff obscures the interesting patterns.

# save some plots that are readable.
pdf(file="VoyClusters2000.pdf",  width=50, height=50)
plot.igraph(f,vertex.size=3, vertex.label=V(f)$W1, vertex.frame.color="grey", vertex.color="white")
dev.off()


pdf(file="VoyClusters1000.pdf",  width=20, height=20)
plot.igraph(g,vertex.size=3, vertex.label=V(g)$W1, vertex.frame.color="grey", vertex.color="white")
dev.off()

# Try some clustering. Didn't get far with this, it's not 
fc <- cluster_fast_greedy(g)
plot(fc, g)
membership(fc)
sizes(fc)

# another way to plot. 
w <- as.matrix(x[1:100,1:2])
plot(graph_from_edgelist(w, directed = FALSE))
w <- graph_from_edgelist(w, directed = FALSE)
plot.igraph(w, vertex.size=3, vertex.frame.color="grey", vertex.color="white", vertex.label=V(w)$W1)

## Another plot of clusters
pdf(file="VoyClusters.pdf",  width=30, height=30)
plot(g, vertex.frame.color="grey", vertex.color="white")
plot.igraph(g,vertex.size=3, vertex.label=V(g)$W1, vertex.frame.color="grey", vertex.color="white")
dev.off()


#########

# Secreta Secretorum neighbors


z <- read.table(file="SSSelf.txt", as.is=TRUE, header=TRUE)
z$Dist2 <- z$Dist * 1000

h <- as.data.frame(z[1:1000,])
c<-graph.data.frame(h, directed=FALSE)

pdf(file="SecClusters1000.pdf",  width=50, height=50)
plot.igraph(c,vertex.size=3, vertex.label=V(f)$W1, vertex.frame.color="grey", vertex.color="white")
dev.off()

## Verumptamen "furthermore" has lots of neighbors. Ignore it.
z <- read.table(file="SSSelfNoVerumptamen.txt", as.is=TRUE, header=TRUE)
z$Dist2 <- z$Dist * 1000

h <- as.data.frame(z[1:1000,])
c<-graph.data.frame(h, directed=FALSE)

pdf(file="SecClusters1000.pdf",  width=50, height=50)
plot.igraph(c,vertex.size=3, vertex.label=V(f)$W1, vertex.frame.color="grey", vertex.color="white")
dev.off()






