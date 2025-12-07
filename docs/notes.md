Notes taken from the paper: [Optimality and Integer Programming Formulations of Triangulations in General Dimension](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1068-11.pdf)

Terms: 
    The stable set problem: https://www.wikiwand.com/en/articles/Independent_set_(graph_theory)
    The set partitioning problem: https://www.wikiwand.com/en/articles/Partition_problem
    
    polytope: https://www.wikiwand.com/en/articles/Polytope
        Polytopes are the generalization of three-dimensional polyhedra to any number of dimensions.
        For example, a two-dimensional polygon is a 2-polytope and a three-dimensional polyhedron is a 3-polytope
        In this context, the sides of a (k + 1)-polytope consist of k-polytopes that may have (k − 1)-polytopes in common.

    convex hull: 
        the smallest convex polytope that encloses a set of points, analogous to stretching a d-dimensional rubber band around the outermost points.
        the convex hull of a d+1 affinely independent points is a d-polytope. => a d-simplex.

        an i-face is the convex hull of a subset of points corresponding to a d-simplex. => an i-face is defined relative to a d-simplex

    affine independence: https://coral.ise.lehigh.edu/~ted/files/ie418/lectures/Lecture4.pdf
        A finite collection of vectors x1, . . . , xk ∈ Rn is affinely
        independent if the vectors x2 − x1, . . . , xk − x1 ∈ Rn are linearly
        independent.
        Linear independence implies affine independence, but not vice versa.
        The property of linear independence is with respect to a given origin.
        Affine independence is essentially a “coordinate-free” version of linear
        independence. 

"Three IP formulations of triangulations are introduced, two based on the stable set problem, and the other based on the set partitioning problem." 
"Some properties that are interesting from a theoretical or practical point of view are considered as objective functions."

"As a result of the recent advances in the performance of computers, the number of applications using triangulation in three dimensions is growing."

"In other words, Delaunay triangulation is not so good in three or more dimensions."

"A $d$-simplex is a $d$-dimensional polytope that is the convex hull of $d+1$ affinely independent points. For example, a line segment, a triangle, and a tetrahedron correspond to a 1-simplex, a 2-simplex, and a 3-simplex, respectively." => in the context of 2D triangulation, a d-simplex is a triangle (2-simplex)

"An $i$
-face of a $d$-simplex is an $\dot{i}$
-simplex $(0\leq\dot{i}\leq d)$ that is the convex hull of a subset of the
vertices of the $d$-simplex. In particular, a $(d-1)$ -face is called a facet." 

"Two $d$-simplices intersect
when the intersection is non-empty and is not a face of at least one of the two simplices."

"In this paper, especially for IP formulations, we consider the division of the convex hull of a point
configuration $A$ of $n$ points in $d$-dimensional space using $d$-simplices, but we use the term
$triangulatin$ for convenience. We assume that $A$ is a configuration in general position (no $d+1$
points lie on the same $(d-1)$ -dimensional hyperplane)."

given A{ a configuration of points in d-dimensional space }
the triangulation of A is: the division of the convex hull of A using d-simplices

triangulation in 2D dimensions is the division of the convex hull (surface) of the set of points into triangules
triangulation in 3D dimensions is the division of the convex hull (volume) of the set of points into polyhedra