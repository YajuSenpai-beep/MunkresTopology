# Metrization Theorems and Paracompactness

The Urysohn metrzation theorem of Chapter 4 was the first step-a giant one-toward an answer to the question: When is a topological space metrizable? It gives conditions under which a space X is metrizable. that it be regular and have a countable basis. But mathematicians are never satusfied with a theorem if there is some hope of proving a stronger one. In the present case,one can hope to strengthen the theorem by finding conditions on X that are both necessary and sufcient for X to be metrizable,that is, conditions that are equivalent to metrizability.

We know that the regularity hypothesis in the Urysohn metrization theorem is a necessary one,but the countable basis condition is not. So the obvious thing to do is try to replace the countable basis condition by something weaker. Finding such conditon is a delicate task. The condition has to be strong enough to imply metrizability,and yet weak enough that all metrzable spaces satisfy it. In a situation like this,discovering the right hypothesis is more than half the battle.

The condition that was eventually formulated,by J. Nagata and Y. Smirnov independently,involves a new notion,that of local finiteness.We say that a collection A of subsets of a space X is locally finite if every point of X has a neighborhood that intersects only finitely many elements of A.

Now one way of expressing the condition that the basis B is countable is to say that B can be expressed in the form

$$
{ \mathcal { B } } = \bigcup _ { n \in \mathbf { Z } _ { + } } { \mathcal { B } } _ { n } ,
$$

where each collection ${ \mathcal { B } } _ { n }$ is finite. This is an awkward way of saying that B is countable,but it suggests how to formulate a weaker version of it.The Nagata-Smirnov condition is to require that the basis B can be expressed in the form

$$
\mathcal { B } = \bigcup _ { n \in \mathbf { Z } _ { + } } \mathcal { B } _ { n } ,
$$

where each collection ${ \mathcal { B } } _ { n }$ is locally finite.We say that such a collection B is countably locally finite. Surpnsingly enough,this condition,along with regulanty,is both necessary and sufficient for metrzability of X. This we shall we prove.

There is another concept in topology that involves the notion of local finiteness. It is a generalization of the concept of compactness called “paracompactness." Although of fairly recent origin, it has proved useful in many parts of mathematics.We introduce it here so that we can give another set of necessary and sufcient conditions for a space X to be metrzable.It turns out that X is metrizable if and only if it is both paracompact and locally metrizable.This we prove in §42.

Some of the sections of this chapter are independent of one another.The dependence among them is expressed in the following diagram.

<!-- image-->

## \$39Local Finiteness

In this sections we prove some elementary properties of locally finite collections and a crucial lemma about metrzable spaces.

Definition. Let X be a topological space. Acollection A of subsets of X is said to be locally finite in X if every point of X hasaneighborhood that intersects only finitely many elements of A

EXAMPLE 1The collection of intervals

$$
\pmb { \mathscr { s } } = \{ ( \mathscr { n } , \mathscr { n } + 2 ) ~ | ~ \mathscr { n } \in \mathbb { Z } \}
$$

is locally finite in the topological space R,as you can check．On the other hand,the collection

$$
\mathcal { B } = \{ ( 0 , 1 / n ) | n \in \mathbb { Z } _ { + } \}
$$

ts locally finite in (O,1) but not in R,as is the collection

$$
\mathfrak { C } = \{ ( 1 / ( n + 1 ) , 1 / n ) \mid n \in \mathbb { Z } _ { + } \}
$$

Lemma 39.1． Let A be a locally finite collection of subsets of X.Then:

(a)Any subcollection of A is locally finite.

(b） The collection $\mathcal { B } = \{ \bar { A } \} _ { A \in \mathcal { A } }$ of the closures ofthe elements of.A is locally finite.

$$
\begin{array} { r } { \overline { { \bigcup _ { A \in \mathcal { A } } { A } } } = \bigcup _ { A \in \mathcal { A } } \bar { A } } \end{array}
$$

Proof._Statement (a) is trvial. To prove (b),note that any open set U that intersects the set $\pmb { \bar { A } }$ necessarily intersects A. Therefore,if U is a neighborhood of x that intersects only finitely many elements Aof A,then U can intersect at most the same number of sets of the collection B. (It might intersect fewer sets of ${ \pmb { \mathcal { B } } } .$ since $\bar { A } _ { 1 }$ and $\bar { A } _ { 2 }$ can be equal even though $\pmb { A } _ { 1 }$ and $A _ { 2 }$ are not).

To prove (c),let Y denote the union of the elements of A:

$$
\bigcup _ { A \in \mathcal { A } } A = Y .
$$

In general, $\cup \bar { A } \subset \bar { Y }$ ：we prove the reverse inclusion,under the assumption of local finiteness. Let $x \in { \bar { Y } }$ ; let U be a neighborhood of x that intersects only finitely many elements of A, say $A _ { 1 } , \ldots , A _ { k }$ .We assert that x belongs to_one of the sets $\bar { A } _ { 1 }$ $\cdots , \bar { A } _ { k }$ 、and hence belongs to $\bigcup { \bar { A } }$ 、For otherwise,the set $\dot { U } - \bar { A } _ { 1 } - \cdots - \bar { A } _ { k }$ would be a neighborhood of x that intersects no element of A and hence does not intersect Y, contrary to the assumption that $\pmb { x } \in \bar { \pmb { \gamma } }$ ■

There is an analogous concept of local finiteness for an indexed famuly of subsets of X.The indexed family $\{ A _ { \alpha } \} _ { \alpha \in J }$ issaid to be a locally finite indexed family in X if every $x \in X$ has a neighborhood that intersects $\pmb { A _ { \alpha } }$ for only finitely many values of α.What is the relation between the two formulations of local finiteness? It is easy to see that $\{ A _ { \alpha } \} _ { \alpha \in J }$ isa locally finite indexed family if and only if it is locally finite as a collection of sets and each nonempty subset A of X equals $A _ { \alpha }$ for at most finitely many values of α.

We shall be concerned with locally finite indexed families only in \$4l,when we deal with partitions of unity.

Definition.A collection B of subsets of X is said to be countably locally finite if B can be written as the countable union of collections ${ \mathcal { B } } _ { n }$ ,each of which is locally finite.

Most authors use the term"g-locally finite" for this concept.Theg comes from measure theory and stands for the phrase "countable union of" Note that both a countable collection and a locally finite collection are countably locally finite.

Definition. Let A be a collection of subsets of the space X. A collection B of subsets of X is said to be a refinement of A (or is said to refine A) if for each element B of B, there is an element A of A containing B.If the elements of B are open sets,we call B an open refinement of A; if they are closed sets,we call B a closed refinement

Lemma 39.2. Let X be a metnzable space. If A is an open covering of X,then there is an open coverng & of X refining A that is countably locally finite.

Proof.We shall use the well-ordering theorem in proving this theorem. Choose a well-ordering <for the collection A.Let us denote the elements of A generically by the letters $U , V , W , \dots$

Choose a metric for X.Let n be a positive integer,fixed for the moment. Given an element U of A,let us define ${ \pmb { \mathscr { S } } } _ { \pmb { \mathscr { n } } } ( U )$ to be the subset of U obtained by“shrinking"U a distance of $1 / n$ More precisely, let

$$
S _ { n } ( U ) = \{ x \mid B ( x , 1 / n ) \subset U \} .
$$

(It happens that $S _ { n } ( U )$ is a closed set, but that is not important for our purposes.） Now we use the well-ordering <of A to pass to a still smaller set.For each U in A,define

$$
T _ { n } ( U ) = S _ { n } ( U ) - \bigcup _ { V < U } V .
$$

The situation where A consists of the three sets $U \ < \ V \ < \ W$ is pictured in Figure 39.1. Just as the figure suggests,the sets we have formed are disjoint.

<!-- image-->  
Figure 39.1

In fact,they are separated by a distance of at least $1 / n$ .This means that if V and W are distinct elements of A,then $d ( x , y ) \geq 1 / n$ whenever $x \in T _ { n } ( V )$ and $y \in T _ { n } ( W )$

To prove this fact,assume the notation has been so chosen that $V \prec W$ . Since x is in $T _ { n } ( V )$ ,then x is in ${ \pmb S } _ { \pmb { n } } ( V )$ ,so the l/n-neighborhood of x lies in V.On the other hand, since $V < W$ and yis in $T _ { n } ( W )$ ,the definition of the latter set tells us that y is not in V. It follows that y is not in the l/n-neighborhood of x.

The sets $T _ { n } ( U )$ are not yet the ones we want,for we do not know that they are open sets.(In fact,they are closed.） So let us expand each of them slightly to obtain an open set ${ \pmb { E } } _ { \pmb { n } } ( U )$ .Specifically, let $E _ { n } ( U )$ be the l/3n-neighborhood of $T _ { \pmb { n } } ( U )$ ; that is,let $E _ { n } ( U )$ be the union of the open balls $B ( x , 1 / 3 n )$ ,for $x \in T _ { n } ( U )$

In the case $U < V < W$ ,we have the situation pictured in Figure 39.2. As the figure suggests,the sets we have formed are disjoint. Indeed,if V and W are distinct elements of $\mathcal { A } ,$ .we assert that $d ( x , y ) \geq 1 / 3 n$ whenever $x \in E _ { n } ( V )$ and $y \in E _ { n } ( W )$ this fact follows at once from the triangle inequality. Note that for each $V \in \mathcal A$ the set $E _ { n } ( V )$ is contained in V.

<!-- image-->  
Figure 39.2

Now let us define

$$
{ \mathcal { E } } _ { n } = \{ E _ { n } ( U ) \mid U \in { \mathcal { A } } \}
$$

We claim that $\pmb { \mathcal { E } _ { n } }$ is a locally finite collection of open sets that refines A．The fact that $\ell _ { n }$ refines A comes from the fact that $E _ { n } ( V ) \subset V$ for each $V \in \mathcal A$ The fact that $\ell _ { n }$ is locally finite comes from the fact that for any x in X,the l/6n-neighborhood of x can intersect at most one element of $\pmb { \mathcal { E } _ { n } }$

Of course,the collection $\mathcal { E } _ { n }$ ,will not cover X. (Figure 392 illustrates that fact.) But we assert that the collection

$$
\mathcal { E } = \bigcup _ { n \in \mathbb { Z } _ { + } } \mathcal { E } _ { n }
$$

does cover X.

Let x be a point of X.The collection A with which we began covers X; let us choose U to be the first element of A (in the well-ordering<)that contains x.Since U is open,we can choose n so that $B ( x , 1 / n ) \subset U$ Then,by definition, $x \in S _ { n } ( U )$ Now because U is the first element of A that contains x,the point x belongs to $T _ { n } ( U )$ · Then x also belongs to the element $E _ { n } ( U )$ of $\mathcal { E } _ { n }$ ,as desired.

## Exercises

1. Check the statements in Example 1.

2.Find a point-finite open covering A of R that is not locally finite. (The collection A is point-finite if each point of R hes in only finitely many elements of A.)

3.Give an example of a collection of sets A that is not locally finite,such that the collection $\pmb { \mathcal { B } } = \{ \bar { A } \ | \ A \in \pmb { \mathcal { A } } \}$ is locally finite.

4.Let A be the following collection of subsets of R:

$$
\pmb { \mathscr { s } } = \{ ( \pmb { n } , \pmb { n } + 2 ) ~ | ~ \pmb { n } \in \mathbb { Z } \}
$$

Which of the following collections refine $\star ?$

$$
{ \mathcal { B } } = \{ ( x , x + 1 ) \mid x \in \mathbb { R } \} ,
$$

$$
{ \mathfrak { C } } = \{ ( n , n + { \frac { 3 } { 2 } } ) \ | \ n \in { \mathbb { Z } } \} ,
$$

$$
\begin{array} { r } { \mathcal { D } = \{ ( x , x + \frac { 3 } { 2 } ) \mid x \in \mathbb { R } \} . } \end{array}
$$

5. Show that if X has a countable basis,a collection A of subsets of X is countably locally finite if and only if it is countable

6.Consider $\mathbb { R } ^ { \omega }$ in the uniform topology. Given n,let ${ \mathcal { B } } _ { n }$ be the collection of all subsets of $\mathbb { R } ^ { \omega }$ of the form $\prod A _ { i }$ ,where $A _ { i } = \mathbb { R }$ for $i \leq n$ and $A _ { i }$ equals either {0} or {l} otherwise.Show that the collection $\mathcal B = \bigcup \mathcal B _ { n }$ is countably locally finite, but neither countable nor locally finite.

## \$40The Nagata-Smirnov Metrization Theorem

Now we prove that regularity of X and the existence of a countably locally finite basis for X are equivalent to metnzability of X.

The proof that these conditions imply metrizability follows very closely the second proof we gave of the Urysohn metrization theorem. In that proof we constructed a map of the space X into $\mathbb { R } ^ { \omega }$ that was an imbedding relative to the uniform metric $\bar { \rho }$ on ${ \mathbb { R } } ^ { \omega }$ So let us review the major elements of that proof. The first step of the proof was to prove that every regular space X with a countable basis is normal．The second step was to construct a countable collection $\{ f _ { n } \}$ of real-valued functons on X that separated points from closed sets. The third step was to use the functions $f _ { n }$ to define a map imbedding X in the product space $\mathbb { R } ^ { \omega }$ . And the fourth step was to show that if $f _ { n } ( x ) \leq 1 / n$ for all x,then this map actually imbeds X in the metrnc space $( \mathbb { R } ^ { \omega } , \bar { \rho } )$

Each of these steps needs to be generalized in order to prove the general metrization theorem.First,we show that a regular space X with a basis that is countably locally finite is normal. Second, we construct a certain collection of real-valued functions $\{ f _ { \alpha } \}$ on X that separates points from closed sets. Third,we use these functions to imbed X in the product space $\mathbb { R } ^ { J }$ ，for some J．And fourth,we show that if the functions $f _ { \alpha }$ are suffciently small,this map actually imbeds X in the metric space $( \mathbb { R } ^ { J } , \bar { \rho } )$

Before we start,we need to recall a notion we have already introduced in the exercises,that of a $G _ { \delta }$ set.

Definition. A subset A of a space X is called a ${ G } _ { \delta }$ set in X if it equals the intersection of a countable collection of open subsets of X.

EXAMPLE l．Each open subset of X is a $G _ { \delta }$ set,irvially In a first-countable Hausdorff space, each one-point set is a $G _ { \delta }$ set The one-point subset (2}of $\bar { s } _ { \Omega }$ is not a $G _ { \delta }$ set, as you can check

EXAMPLE 2In a metric space X,each closed set is a $G _ { \delta }$ set. Given $A \subset X$ ,let $U ( A , \epsilon )$ denote the ε-neighborhood of A If A is closed, you can check that

$$
A = \bigcap _ { n \in \mathbf { Z } _ { + } } U ( A , 1 / n )
$$

Lemma 40.l. Let X be a regular space with a basis B that is countably locally finite. Then X is normal,and every closed set in X is a $G _ { \delta }$ set in X

Proof.Step 1. Let W be open in X.We show there is a countable collection $\{ U _ { n } \}$ of open sets of X such that

$$
W = \bigcup U _ { n } = \bigcup \bar { U } _ { n } .
$$

Since the basis B for X is countably locally finite,we can write $\mathcal B = \bigcup \mathcal B _ { n }$ ,where each collection ${ \mathcal { B } } _ { n }$ is locally finite.Let ${ \mathcal { C } } _ { n }$ be the collection of those basis elements B such that $B \in { \mathcal { B } } _ { n }$ and $\bar { B } \subset W$ . Then ${ \mathfrak { C } } _ { \mathfrak { n } }$ is locally finite,being a subcollection of ${ \mathcal { B } } _ { n }$ Define

$$
U _ { n } = \bigcup _ { B \in \mathcal { C } _ { n } } B .
$$

Then $U _ { n }$ is an open set,and by Lemma 39 1,

$$
\bar { U } _ { n } = \bigcup _ { B \in \mathcal { C } _ { n } } \bar { B } .
$$

Therefore, $\bar { U } _ { n } \subset W$ ,so that

$$
\bigcup U _ { n } \subset \bigcup \bar { U } _ { n } \subset W
$$

We assert that equality holds.Given $\textit { \textbf { x } } \in \textit { \textbf { W } }$ ,thereis byregularitya basis element $B \in \mathcal { B }$ such that $\textsf { \pmb { x } } \in \textsf { \pmb { B } }$ and $\bar { B } \subset W$ . Now $B \in \mathcal { B } _ { n }$ for some n.Then $B \in { \mathcal { C } } _ { n }$ by definition, so that $x \in U _ { n }$ . Thus $W \subset \bigcup U _ { n }$ ,as desired.

Step 2.We show that every closed set C in X is a $G _ { \delta }$ set in X Given C,let $w = x - C$ .By Step l,there are sets $U _ { n }$ in X such that $W = \bigcup \bar { U } _ { n }$ Then

$$
C = \bigcap ( X - { \bar { U } } _ { n } ) ,
$$

so that C equals a countable intersection of open sets of X.

Step 3.We show X is normal Let Cand D be disjoint closed sets in X.Applying Step l to the open set $\pmb { X } - \pmb { D }$ ，we construct a countable collection $\{ U _ { n } \}$ of open sets such that $\bigcup U _ { n } = \bigcup { \bar { U } } _ { n } = X - D$ Then $\{ U _ { n } \}$ covers C and each set $\bar { U } _ { n }$ is disjoint from D.Similarly, there is a countable covering $\{ V _ { n } \}$ of D by open sets whose closures are disjoint from C.

Now we are back in fhe situation that arose in the proof that a regular space with a countable basis is normal (Theorem 32.1).We can repeat that proof verbatim. Define

$$
U _ { n } ^ { \prime } = U _ { n } - \bigcup _ { i = 1 } ^ { n } { \bar { V } } _ { i } \quad \quad { \mathrm { a n d } } \quad V _ { n } ^ { \prime } = V _ { n } - \bigcup _ { i = 1 } ^ { n } { \bar { U } } _ { i }
$$

Then the sets

$$
U ^ { \prime } = \bigcup _ { n \in \mathbb { Z } _ { + } } U _ { n } ^ { \prime } \mathrm { a n d } V ^ { \prime } = \bigcup _ { n \in \mathbb { Z } _ { + } } V _ { n } ^ { \prime }
$$

are disjoint open sets about C and D,respectively.

Lemma 40.2. Let X be normal;let A be a closed $G _ { \delta }$ set in X．Then there is a continuous function $f \cdot X  [ 0 , 1 ]$ such that $f ( x ) = 0$ for $x \in A$ and $f ( x ) > 0$ for x A.

Proof.We gave this as an exercise in &33,we provide a proof here. Write A as the intersection of the open sets $U _ { n }$ ,for $\pmb { n } \in \mathbb { Z } _ { + }$ For each n,choose a continuous function $f _ { n } : X \to [ 0 , 1 ]$ such that $f ( x ) = 0$ for $x \in A$ and $f ( x ) = 1$ for $x \in X - U _ { n }$ Define $\textstyle f ( x ) = \sum f _ { n } ( x ) / 2 ^ { n }$ The series converges uniformly,by comparison with $\sum 1 / 2 ^ { n }$ ， so that f is continuous.Also,f vanishes on A and is positive on $X - A$

Theorem 40.3 (Nagata-Smirnov metrization theorem). A space X 1s metrizable if andonlyifXisregularand hasa basis that is countably locallyfinite.

Proof.Step l.Assume X is regular with a countably locally finite basis B Then X is normal,and every closed set in X is a $G _ { \delta }$ set in X.We shall show that X is metrizable by imbedding X in the metric space $( \mathbb { R } ^ { J } , \bar { \rho } )$ for some J

Let $\mathcal B = \bigcup \mathcal B _ { n }$ ，where each collection ${ \mathcal { B } } _ { n }$ is locally finite.For each positive integern,and each basis element $B \in { \mathcal { B } } _ { n }$ ,choose a continuous function

$$
f _ { n , B } \cdot X \longrightarrow [ 0 , 1 / n ]
$$

such that $f _ { n , B } ( x ) > 0$ for $x \in B$ and $f _ { n , B } ( x ) = 0$ for $x \notin B$ . The collecuon $\{ f _ { n , B } \}$ separates points from closed sets in X. Given a point xo and a neighborhood U of xo, there isa basiselementB such that $x _ { 0 } \in B \subset U$ . Then $B \in { \mathcal { B } } _ { n }$ for some n,so that $f _ { n , B } ( x _ { 0 } ) > 0$ and $f _ { n , B }$ vanishes outside U.

Let J be the subset of $\mathbb { Z } _ { + } \times \mathbf { \mathcal { B } }$ consisting of all pairs $( n , B )$ such that B is an element of ${ \mathcal { B } } _ { n }$ . Define

$$
F : X \longrightarrow [ 0 , 1 ] ^ { J }
$$

by the equation

$$
F ( x ) = ( f _ { n , B } ( x ) ) _ { ( n , b ) \in J } .
$$

Relative to the product topology on $[ 0 , 1 ] ^ { J }$ ，the map $_ { F }$ is an imbedding，by Theorem 34.2.

Now we give $[ 0 , 1 \} ^ { J }$ the topology induced by the uniform metric and show that F is an imbedding relative to this topology as well.Here is where the condition $f _ { n , B } ( x ) ~ < ~ 1 / n$ comes in. The uniform topology is finer (larger) than the product topology. Therefore,relative to the uniform metric,the map F is injective and carries open sets of X onto open sets of the image space $Z = F ( X )$ We must give a separate proof that F is continuous.

Note that on the subspace $[ 0 , 1 ] ^ { J }$ of $\mathbb { R } ^ { J }$ , the uniform metric equals the metric

$$
\rho ( ( x _ { \alpha } ) , ( y _ { \alpha } ) ) = \mathsf { s u p } \{ | x _ { \alpha } - y _ { \alpha } | \} .
$$

To prove conunuity, we take a point $\pmb { x } _ { \mathbf { 0 } }$ of X and a number $\epsilon > 0 .$ ,and find a neighborhood W of $\pmb { x } _ { \pmb { 0 } }$ such that

$$
x \in W \Longrightarrow \rho ( F ( x ) , F ( x _ { 0 } ) ) < \epsilon
$$

Let n be fixed for the moment. Choose a neighborhood $U _ { \pmb { n } }$ of $\scriptstyle x _ { 0 }$ that intersects only finitely many elements of the collection ${ \mathcal { B } } _ { \pmb { n } }$ . This means that as B ranges over ${ \mathcal { B } } _ { n }$ all but finitely many of the functions $f _ { n , B }$ are identically equal to zero on $U _ { \pmb { n } }$ . Because each function $f _ { n , B }$ is continuous,we can now choose a neighborhood $V _ { n }$ of $x _ { 0 }$ contained in $U _ { n }$ on which each of the remaining functions $f _ { n , B }$ ,for $B \in { \mathcal { B } } _ { n }$ , varies by at most $\epsilon / 2$

Choose such a neighborhood $V _ { \pmb { \pi } }$ of $x _ { 0 }$ for each $\pmb { n } \in \mathbb { Z } _ { + }$ .Then choose N so that $1 / N \le \epsilon / 2$ ,and define $W = V _ { 1 } \cap \cdots \cap V _ { N }$ We assert that W is the desired neighborhood of xo. Let $x \in W$ .If $n \leq N$ , then

$$
| f _ { n , B } ( x ) - f _ { n , B } ( x _ { 0 } ) | \leq \epsilon / 2
$$

because the function $f _ { n , B }$ either vanishes identically or varies by at most $\epsilon / 2$ on W. If $\pmb { n } > N$ ,then

$$
| f _ { n , B } ( x ) - f _ { n , B } ( x _ { 0 } ) | \leq 1 / n < \epsilon / 2
$$

because $f _ { n , B }$ maps X into $[ 0 , 1 / n ]$ .Therefore,

$$
\rho ( F ( x ) , F ( x _ { 0 } ) ) \le \epsilon / 2 < \epsilon ,
$$

as desired.

Step 2.Now we prove the converse. Assume X is metrizable. We know X is regular; let us show that X has a basis that is countably locally finite.

Choose a metric for X.Given m,let $\star _ { m }$ be the covering of X by all open balls of radius $1 / m$ .By Lemma 39.2,there is an open covering ${ \mathcal { B } } _ { m }$ of X refining $\star _ { m }$ such that ${ \mathcal { B } } _ { m }$ is countably locally finite.Note that each element of ${ \mathcal { B } } _ { m }$ has diameter at most $2 / m$ Let B be the union of the collections ${ \mathcal { B } } _ { m }$ ,for $m \in \mathbb { Z } _ { + }$ ．Because each collection ${ \mathcal { B } } _ { m }$ is countably locally finite,so isB.We show that B isa basis for X.

Given $x \in { \pmb { X } }$ and given $\epsilon > 0$ ,we show that there is an element B of B containing x that is contained in $B ( x , \epsilon )$ .First choose m so that $1 / m < \epsilon / 2$ .Then,because ${ \mathcal { B } } _ { m }$ covers X,we can choose an element B of ${ \mathcal { B } } _ { m }$ that contains x.Since B contains x and has diameter at most $2 / m < \epsilon$ , it is contained in $\pmb { { \cal B } } ( \pmb { x } , \epsilon )$ ,as desired. ■

## Exercises

1. Check the details of Examples l and 2.

2.A subset W of X is said to be an $\ " \mathbf { F } _ { \pmb { \sigma } }$ set"in X if W equals a countable union of closed sets of X. Show that W is an ${ \pmb F } _ { { \pmb \sigma } }$ set in Xif and only if $\pmb { \chi } - \pmb { W }$ is a $G _ { \delta }$ set in X.

[The termunology comes from the French. The“F" stands for“ferme,"which means“closed,"and the“g" for“somme."which means “union."]

3.Many spaces have countable bases;but no $T _ { 1 }$ space has a locally finite basis unless it is discrete.Prove this fact.

4.Find a nondiscrete space that has a countably locally finite basis but does not have a countable basis.

5.A collection A of subsets of X is said to be locally discrete if each point of X has a neighborhood that intersects at most one element of A.A collection B is countably locally discrete (or “g-locally discrete") if it equals a countable union of locally discrete collections.Prove the following:

Theorem (Bing metrization theorem).A space X is metrizable if and only if it is regular and hasa basis that iscountably locally discrete.

## \$41 Paracompactness

The concept of paracompactness is one of the most useful generalizations of compactness that has been discovered in recent years. It is particularly useful for applications in topology and differential geometry We shall give just one application,a metrization theorem that we prove in the next section.

Many of the spaces that are familiar to us already are paracompact. For instance, every compact space is paracompact,this will be an immediate consequence of the definition. It is also true that every metrizable space is paracompact,this is a theorem due to A.H. Stone,which we shall prove. Thus the class of paracompact spaces includes the two most important classes of spaces we have studied. It includes many other spaces as well.

To see how paracompactness generalizes compactness, we recall the de finition of compactness: A space X is said to be compact if every open covering A of X contains a finite subcollection that covers X.An equivalent way ofsaying this is the following:

A space X is compact if every open covering A of X has a finite open refinement B that covers X

This definition is equivalent to the usual one,given such a refinement B,one can choose for each element of B an element of A containing it; in this way one obtains a finite subcollection of A that covers X.

This new formulation of compactness is an awkward one,but it suggests a way to generalize.

Definition.  A space X is paracompact if every open covering A of X has a locally finite open refinement B that covers X.

Many authors,following the lead of Bourbaki,include as part of the definition of the term paracompact the requirement that the space be Hausdorff.(Bourbaki also includes the Hausdorff condition as part of the definition of the term compact.） We shall not follow this convention.

EXAMPLE 1．The space $\pmb { \mathbb { R } } ^ { n }$ is paracompaci Let $\pmb { X } = \pmb { \mathbb { R } } ^ { n }$ Let A be an open covening of X. Let $B _ { 0 } = \emptyset$ ,and for each positive integer m,let $B _ { m }$ denote the open ball of radius m centered at the orgin. Given m,choose finitely many elements of $\mathbf { \star }$ that cover $\scriptstyle { \vec { B } } _ { m }$ and intersect each one with the open set $X \mathrm { ~ - ~ } \bar { B } _ { m - 1 }$ ,let this finite collection of open sets be denoted ${ \mathfrak { C } } _ { m }$ Then the collection $\mathscr { C } = \bigcup \mathscr { C } _ { m }$ is arefinement of A It is clearly locally finite, for the open set $\pmb { B _ { m } }$ intersects only finitely many elements of C,namely those elements belonging to the collection $\mathcal { C } _ { 1 } \cup \quad \cup \mathcal { C } _ { m }$ .Finally.Ccovers X For,given x,let m be the smallest integer such that $\boldsymbol { x } \in \bar { \boldsymbol { B } } _ { m }$ Then x belongs to an element of ${ \mathcal { C } } _ { m }$ ,by definition.

Some of the properties of a paracompact space are similar to those of a compact space.For instance,a subspace of a paracompact space is not necessarily paracompact; but a closed subspace is paracompact. Also,a paracompact Hausdorff space is normal. In other ways,a paracompact space is not similar to a compact space; in particular, the product of two paracompact spaces need not be paracompact. We shall verify these facts shortly.

## Theorem 41.1．Every paracompact Hausdorff space X is normal

ProofThe proof is somewhat simular to the proof that a compact Hausdorff space is normal.

First one proves regularity Let a be a point of X and let B be a closed set of X disjoint from a. The Hausdorfcondition enables us to choose,for each b in B,an open set $U _ { b }$ about b whose closure is disjoint from a. Cover X by the open sets $U _ { b }$ , along with the open set $\pmb { \chi } - \pmb { B }$ ：takea locally finite open refinement C that covers X.Form the subcollection D of C consisting of every element of C that intersects B.Then D covers B.Furthermore,if $\pmb { D } \in \mathcal { D }$ ，then $\bar { D }$ is disjoint from a.For D intersects B,so it lies in some set $U _ { b }$ ,whose closure is disjoint from a. Let

$$
V = \bigcup _ { D \in \mathcal { D } } D ;
$$

then V is an open set in X containing B.Because $\mathcal { D }$ is locally finite,

$$
\bar { V } = \bigcup _ { D \in \mathcal { D } } \bar { D } ,
$$

so that $\bar { \nu }$ is disjoint from a. Thus regularity is proved.

To prove normality, one merely repeats the same argument,replacing a by the closed set A throughout and replacing the Hausdorff condituon by regularnty. □

## Theorem 41.2. Every closed subspace of a paracompact space is paracompact.

Proof.Let Y be a closed subspace of the paracompact space X; let A be a covering of Y by sets open in Y. For each $A \in \mathcal A$ ，choose an open set $A ^ { \prime }$ of X such that $A ^ { \prime } \cap Y = A$ Cover X by the open sets A',along with the open set X-Y.Let B be a locally finite open refinement of this covering that covers X.The collection

$$
{ \mathcal { C } } = \{ B \cap Y \mid B \in { \mathcal { B } } \}
$$

is the required locally finite open refinement of A

EXAMPLE 2. A paracompacl subspace ofa Hausdorf space X need not be closed in X. Inded,ihe open inierval (O,1）is paracompacl,being homeomorphic IoR,bul it is nol closed in R

EXAMPLE 3A subspace of a paracompact space need not be paracompaci The space $\bar { s } _ { \Omega } \times \bar { s } _ { \Omega }$ is compacl and,iherefore,paracompaci. Bul ihe subspace $\pmb { S } _ { \Omega } \times \dot { \pmb { S } } _ { \Omega }$ is nol para-Compaci,for it is Hausdorff bul nol normal.

To prove the important theorem that every metrizable space is paracompact, we need the following lemma,due to E. Michael, which is also useful for other purposes:

Lemma 41.3.Let X be regular. Then the following conditions on X are equivalent: Every open coverng of X has a refinement that is:

(l）An open covenng of X and countably locally finite.

(2)A covenng of X and locally finite.

(3）A closed covering of X and locally finite.

(4) An open covering of X and locally finite.

Proof.It is trivial that $( 4 ) \Rightarrow ( 1 )$ . What we need to prove our theorem is the converse In order to prove the converse,we must go through the steps $( 1 ) \Rightarrow ( 2 ) \Rightarrow ( 3 ) \Rightarrow ( 4 )$ anyway,so we have for convenience listed these conditions in the statement of the lemma.

(1)= (2). Let A be an open covering of X. Let B be an open refinement of A that covers X and is countably locally finite; let

$$
\mathcal B = \bigcup \mathcal B _ { n }
$$

where each ${ \mathcal { B } } _ { \mathfrak { n } }$ is locally finite.

Now we apply essentially the same sort of shrnking trick we have used before to make sets from different $\mathcal { B } _ { n } \mathrm { ~ \bf ~ s ~ }$ disjoint. Given i,let

$$
V _ { i } = \bigcup _ { U \in \mathcal { B } _ { \boldsymbol { r } } } U .
$$

Then for each $\pmb { n } \in \mathbb { Z } _ { + }$ and each element U of ${ \mathcal { B } } _ { n }$ ,define

$$
S _ { n } ( U ) = U - \bigcup _ { i < n } V _ { i } .
$$

[Note that ${ \pmb { \mathscr { S } } } _ { \pmb { \mathscr { n } } } ( U )$ is not necessarily open, nor closed.] Let

$$
{ \mathcal { C } } _ { n } = \{ S _ { n } ( U ) \mid U \in { \mathcal { B } } _ { n } \} .
$$

Then $\mathcal { C } _ { n }$ is a refinement of ${ \mathcal { B } } _ { n }$ , because $S _ { n } ( U ) \subset U$ for each $U \in { \mathcal { B } } _ { n }$

Let ${ \mathcal { C } } = \bigcup { \mathcal { C } } _ { n }$ . We assert that C is the required locally finite refinement of A, covering X

Let x be a point of X．We wish to prove that x lies in an element of C,and that x has a neighborhood intersecting only finitely many elements of C.Consider the covering $\mathcal B = \bigcup \mathcal B _ { n }$ ; let N be the smallest integer such that x lies in an element of ${ \mathcal { B } } _ { N }$ Let U be an element of ${ \mathcal { B } } _ { N }$ containing x.First, note that since x lies in no element of ${ \mathcal { B } } _ { i }$ for $i < N$ ,the point x lies in the element ${ \pmb S } _ { N } ( U )$ of C.Second, note that since each collection ${ \mathcal { B } } _ { n }$ is locally finite,we can choose for each $\pmb { n } = 1 , \ldots , \pmb { N }$ a neighborhood ${ \pmb W } _ { \pmb n }$ of x that intersects only finitely many elements of ${ \mathcal { B } } _ { n }$ .Now if ${ \pmb W } _ { \pmb { \eta } }$ intersects the element ${ \pmb S } _ { \pmb { n } } ( V )$ of $\mathcal { C } _ { n }$ ,it must intersect the element V of ${ \mathcal { B } } _ { n }$ ,since $S _ { n } ( V ) \subset V$ Therefore, ${ \pmb w } _ { \pmb n }$ intersects only finitely many elements of $\mathfrak { C } _ { \pmb { n } }$ .Furthermore,because U is in ${ \mathcal { B } } _ { N }$ ,U intersects no element of $\mathcal { C } _ { \mathfrak { n } }$ for $n > N$ Asa result,the neighbo rhood

$$
W _ { 1 } \cap W _ { 2 } \cap \cdots \cap W _ { N } \cap U
$$

of x intersects only finitely many elements of C.

(2)=(3) Let A be an open covering of X.Let B be the collection of all open sets U of X such that $\bar { U }$ is contained in an element of A.By regularity,B covers X. Using (2), we can find a refinement C of B that covers X and is locally finite. Let

$$
{ \mathcal { D } } = \{ { \bar { C } } | C \in { \mathcal { C } } \} .
$$

Then D also covers X; it is locally finite by Lemma 39.1; and it refines A.

(3)= (4). Let A be an open covering of X. Using (3),choose B to be a refinement of A that covers X and is locally finite (We can take B to be a closed refinement if we like,but that is irrelevant.） We seek to expand each element B of B slightly to an open set, making the expansion slight enough that the resulting collection of open sets will still be locally finite and will still refine A.

This step involves a new trick. The previous trick,used several times, consisted of ordering the sets in some way and forming a new set by subtracting off all the previous ones.That trick shrinks the sets; to expand them we need something different. We shall introduce an auxiliary locally finite closed covering C of X and use it to expand the elements ofB.

For each point x of X,there is a neighborhood of x that intersects only finitely many elements of B. The collection of all open sets that intersect only finitely many elements of B is thus an open covering of X．Using (3）again,let C be a closed refinement of this covering that covers X and is locally finite. Each element of C intersects only finitely many elements of B.

For each element B of B,let

$$
{ \mathfrak { C } } ( B ) = \{ C \mid C \in { \mathcal { C } } { \mathrm { ~ a n d ~ } } C \subset X - B \}
$$

Then define

$$
E ( B ) = X - \bigcup _ { C \in \mathcal { C } ( B ) } C .
$$

Because C is a locally finite collection of closed sets,the union of the elements of any subcollection of C is closed,by Lemma 39.1. Therefore,the set E(B) is an open set. Furthermore, $E ( B ) \supset B$ by definition.(See Figure 4l 1,in which the elements of B are represented as closed circular regions and line segments,and the elements of C are represented as closed square regions.)

<!-- image-->  
Figure 41.1

Now we may have expanded each B too much; the collection $\{ E ( B ) \}$ may not be a refinement of A.This is easily remedied.For each $B \in { \mathcal { B } }$ ,choose an elerment ${ \pmb F } ( { \pmb B } )$ of A containing B.Then define

$$
{ \mathcal { D } } = \{ E ( B ) \cap F ( B ) \mid B \in { \mathcal { B } } \} .
$$

The collection $\pmb { \mathcal { D } }$ is a refinement of A. Because $B \subset ( E ( B ) \cap F ( B ) )$ and B covers X, the collection D also covers X

We have finally to prove that $\mathbfcal { D }$ is locally finite. Given a point x of X,choose a neighborhood W of x that intersects only finitely many elements of C,say $C _ { 1 } , \ldots , C _ { k }$ We show that W intersects only finitely many elements of D.Because C covers X, the set W is covered by ${ \cal C } _ { 1 } , \dots , { \cal C } _ { k }$ .Thus, it suffices to show that each element C of C intersects only finitely many elements of $\pmb { \mathcal { D } }$ .Now if C intersects the set $E ( B ) \cap F ( B )$ then it intersects ${ \pmb E } ( { \pmb B } )$ ,so by definition of $E ( B )$ it is not contained in $\pmb { \chi } - \pmb { B }$ ,hence C must intersect B.Since C intersects only finitely many elements of B,it can intersect at most the same number of elements of the collection $\pmb { \mathcal { D } }$ □

## Theorem 41.4. Every metrizable space is paracompact

Proof.Let X be a metrizable space. We already know from Lemma 39.2 that, given an open covering A of X,it has an open refinement that covers X and is countably locally finite. The preceding lemma then implies that A has an open refinement that covers Xand is locally finite

## Theorem 41.5.Every regular Lindelof space is paracompact

ProofLet X be regular and Lindelof. Given an open covering A of X,it has a countable subcollection that covers X,this subcollection is automatically countably locally finite The preceding lemma applies to show A has an open refinement that covers Xand is locally finite.

EXAMPLE 4The product of two paracompact spaces need not be paracompact The space $\mathbb { R } _ { \ell }$ is paracompact,for it is regular and Lindelof However. $\mathbb { R } _ { \ell } \times \mathbb { R } _ { \ell }$ is not paracompact,for it is Hausdorff but not normal

EXAMPLE5.The space $\mathbb { R } ^ { \omega }$ is paracompact in both the product and uniform topologies. This result follows from the fact that $\mathbb { R } ^ { \omega }$ is metrizable in these topologies.It is not known whether $\mathbb { R } ^ { \omega }$ is paracoipact in the box topology (See the comment in Exercise 5of \$32）

EXAMPLE 6. The product space $\mathbb { R } ^ { J }$ is not paracompact if Jis uncountable For $\mathbb { R } ^ { J }$ is Hausdorff but not normal

One of the most useful properties that a paracompact space X possesses has to do with the existence of partitions of unity on X.We have already seen the firite version of this notion in \$36,we discuss the general case now. Recall that if $\phi \cdot \chi \to { \mathbb { R } }$ ,the support of $\phi$ is the closure of the set ot those x for which $\phi ( { \pmb x } ) \neq 0$

Definition. Let $\{ U _ { \alpha } \} _ { \alpha \in J }$ be an indexed open covering of X.An indexed famuly of continuous functions

$$
\phi _ { \alpha } : X \to [ 0 , 1 ]
$$

is said to be a partition of unity on X,dominated by $\{ U _ { \alpha } \}$ ,if:

（1） (Support $\phi _ { \alpha } ) \subset U _ { \alpha }$ for each α.

(2）The indexed famuly {Support $\phi _ { \alpha } \}$ is locally finite

(3) $\sum \phi _ { \alpha } ( x ) = 1$ for each x.

Condition (2) implies that each $x \in X$ has a neighborhood on which the function $\phi _ { \pmb { \alpha } }$ vanishes identically for all but finitely many values of α.Thus we can make sense of the "sum" indicated in (3); we interpret it to mean the sum of the terms $\phi _ { \pmb { \alpha } } ( \pmb { x } )$ that do not equal zero.

We now construct a partition of unity on an arbitrary paracompact Hausdorff space.We begin by proving a“shrinking lemma,’ just as we did for the finite case in \$36.

\*Lemma 41.6. Let X be a paracompact Hausdorff space; let $\{ U _ { \alpha } \} _ { \alpha \in J }$ be an indexed family of open sets covering X.Then there exists a locally finite indexed family $\{ V _ { \alpha } \} _ { \alpha \in J }$ of open sets covering X such that $\bar { V } _ { \alpha } \subset U _ { \alpha }$ for each α.

The condition that $\tilde { V } _ { \alpha } \subset U _ { \alpha }$ for each α is sometimes expressed by saying that the famuly $\{ \bar { V } _ { \alpha } \}$ is aprecise refinement of the family $\{ U _ { \alpha } \}$

Proof.Let A be the collection of all open sets A such that $\bar { A }$ is contained in some element of the collection $\{ U _ { \pmb { \alpha } } \}$ .Regularity of X implies that A covers X.Since X is paracompact,we can find a locally finite collection $\pmb { \mathcal { B } }$ of open sets covering X that refines A Let us index B bijectively with some index set K,then the general element of B can be denoted $\pmb { { \cal B } } _ { \pmb { \beta } }$ for $\beta \in K$ ,and $\{ B _ { \beta } \} _ { \beta \in K }$ is a locally finite indexed famuly. Since $\pmb { \mathcal { B } }$ refinesA,we can define a function $f : K \to J$ by choosing,for each $\beta$ in K, an element $f ( \beta ) \in J$ such that

$$
\bar { B } _ { \beta } \subset U _ { f ( \beta ) } .
$$

Then for each $\pmb { \alpha } \in \pmb { J }$ , we define $V _ { \pmb { \alpha } }$ to be the union of the elements of the collection

$$
{ \mathcal { B } } _ { \alpha } = \{ B _ { \beta } \mid f ( \beta ) = \alpha \} .
$$

(Note that $V _ { \pmb { \alpha } }$ is empty if there exists no index β such that $f ( \beta ) = \alpha . )$ For each element $B _ { \beta }$ of the collection $\mathcal { B } _ { \pmb { \alpha } }$ we have $\bar { \pmb { { B _ { \beta } } } } \subset U _ { \pmb { \alpha } }$ by definition. Because the collection $\mathcal { B } _ { \pmb { \alpha } }$ is locally finite, $\bar { V } _ { \pmb { \alpha } }$ equals the union of the closures of the elements of $\mathcal { B } _ { \pmb { \alpha } }$ ,s0 that $\bar { V } _ { \alpha } \subset U _ { \alpha }$

Finally,we check local finiteness Given $x \in X$ ,choose a neighborhood W of x such that W intersects $\pmb { { \cal B } } _ { \pmb { \beta } }$ for only finitely many values of $\pmb { \beta }$ say $\pmb { \beta } = \pmb { \beta } _ { 1 } , \ldots , \pmb { \beta } _ { K }$ Then W can intersect $V _ { \pmb { \alpha } }$ only if α is one of the indices $f ( \beta _ { 1 } ) , \dots , f ( \beta _ { K } )$

\*Theorem 41.7. Let X be a paracompact Hausdorff space; let $\{ U _ { \alpha } \} _ { \alpha \in J }$ be an indexed open covering of X. Then there exists apartition of unity on X dominated by $\{ U _ { \alpha } \}$

Proof.We begin by applying the shrinking lemma twice,to find locally finite indexed familes of open sets $\{ W _ { \pmb { \alpha } } \}$ and $\{ V _ { \pmb { \alpha } } \}$ covering X,such that $\overline { { W } } _ { \alpha } \subset V _ { \alpha }$ and $\bar { V } _ { \alpha } \subset U _ { \alpha }$ for each α Since X is normal,we may choose,for each α,a continuous function $\psi _ { \alpha } : X \to [ 0 , 1 ]$ such that $\psi _ { \alpha } ( \overline { { W } } _ { \alpha } ) = \{ 1 \}$ and $\psi _ { \alpha } ( X - V _ { \alpha } ) = \{ 0 \}$ . Since $\psi _ { \pmb { \alpha } }$ is nonzero only at points of $V _ { \pmb { \alpha } }$ ,we have

$$
( \mathsf { S u p p o r t } \psi _ { \alpha } ) \subset \bar { V } _ { \alpha } \subset U _ { \alpha } .
$$

Furthermore,the indexed family $\{ \bar { V } _ { \alpha } \}$ is locally finite (since an open set intersects $\bar { V } _ { \pmb { \alpha } }$ only if it intersects $V _ { \pmb { \alpha } } ) ^ { \cdot }$ ；hence the indexed family {Support $\psi _ { \pmb { \alpha } } \}$ is also locally finite. Note that because $\{ W _ { \pmb { \alpha } } \}$ covers X,for any given x at least one of the functions $\psi _ { \pmb { \alpha } }$ is positive at x.

We can now make sense of the formally infinite sum

$$
\Psi ( x ) = \sum _ { \alpha } \psi _ { \alpha } ( x )
$$

Since each $\textbf { \textit { x } } \in \textbf { \textit { X } }$ hasa neighborhood $W _ { x }$ that intersects the set (Support $\psi _ { \pmb { \alpha } } )$ for only finitely many values of α,we can interpret this infinite sum to mean the sum of its (finitely many） nonzero terms. It follows that the restriction of Ψ to $W _ { x }$ equals a finite sum of continuous functions,and is thus continuous.Then since $\Psi$ is continuous on $W _ { x }$ for each x,it is continuous on X.It is also positive.We now define

$$
\phi _ { \alpha } ( x ) = \psi _ { \alpha } ( x ) / \Psi ( x )
$$

to obtan our desired partition of unity.

Partitions of unity are most often used in mathematics to “patch together” functions that are defined locally so as to obtain a function that is defined globally. Their use in §36 illustrates this process. Here is another such illustration'

\*Theorem 41.8. Let X be a paracompact Hausdorff space: let C be a collection of subsets of X;for each $C \in { \mathcal { C } }$ let $\epsilon _ { C }$ be a positive number $\pmb { I f } \pmb { C }$ is locally finite,there is a continuous function $f : X \to \mathbb { R }$ such that $f ( x ) > 0$ forall x,and $f ( x ) \leq \epsilon _ { C }$ for $x \in C$

Proof.Cover X by open sets each of which intersects at most finitely many elements of C; index this collction of open sets so that it becomes an indexed family $\{ U _ { \alpha } \} _ { \alpha \in J }$ Choose a partition of unity $\{ \phi _ { \alpha } \}$ on X dominated by $\{ U _ { \alpha } \}$ Given ${ \pmb { \alpha } } ,$ let $\delta _ { \pmb { \alpha } }$ be the minimum of the numbers $\epsilon _ { C }$ ,as C ranges over all those elements of C that intersect the support of $\phi _ { \pmb { \alpha } }$ ,if there are no such elements of C,set $\delta _ { \pmb { \alpha } } = 1$ . Then define

$$
f ( x ) = \sum \delta _ { \alpha } \phi _ { \alpha } ( x ) .
$$

Because all the numbers $\delta _ { \alpha }$ are positive,so is f.We show that $f ( x ) \leq \epsilon _ { C }$ for ${ \pmb x } \in C$ It will suffice to show that for ${ \pmb x } \in C$ and arbitrary α,we have

$$
\delta _ { \alpha } \phi _ { \alpha } ( x ) \leq \epsilon _ { C } \phi _ { \alpha } ( x ) ;\tag{*}
$$

then the desired inequality follows by summing,as $\sum \phi _ { \alpha } ( x ) = 1$ . If x 4 Support Φα, then inequality(\*） is trivial because $\phi _ { \pmb { \alpha } } ( \pmb { x } ) = 0$ And if $x \in \ S \mathbf { u p p o r t } \phi _ { \alpha }$ and x $\in { \mathfrak { C } }$ then C intersects the support of $\phi _ { \pmb { \alpha } }$ , so that $\delta _ { \pmb { \alpha } } \leq \epsilon _ { C }$ by construction; thus(\*） holds.

## Exercises

1. Give an example to show that if X is paracompact, it does not follow that for every open covering A of X,there is a locally finite subcollection of A that covers X.

2.(a) Show that the product of a paracompact space and a compact space is paracompact. [Hint: Use the tube lemma.]

(b） Conclude that $\pmb { S } _ { \Omega }$ is not paracompact.

3. Is every locally compact Hausdorff space paracompact?

4. (a) Show that if X has the discrete topology,then X is paracompact.

(b） Show that if $f : X \to Y$ is continuous and X is paracompact,the subspace $f ( X )$ of Y need not be paracompact.

5.Let X be paracompact. We proved a “shrinking lemma"for arbitrary indexed open coverings of X. Here is an "expansion lemma" for arbitrary locally finite indexed families in X.

Lemma. Let $\{ B _ { \alpha } \} _ { \alpha \in J }$ bea locally finite indexed family of subsets of the paracompact Hausdorff space X.Then there isa locally finite indexed family $\{ U _ { \alpha } \} _ { \alpha \in J }$ of open sets in X such that $B _ { \alpha } \subset U _ { \alpha }$ for each α.

6. (a)Let X be a regular space. If X is a countable union of compact subspaces of X,then X is paracompact.

(b） Show $\mathbb { R } ^ { \infty }$ is paracompact as a subspace of $\mathbb { R } ^ { \omega }$ in the box topology.

\*7. Let X be a regular space.

(a) If X is a finite union of closed paracompact subspaces of X,then X is paracompact.

(b) If X is a countable union of closed paracompact subspaces of X whose interiors cover X,show Xis paracompact.

8. Let $p : X \to Y$ be a perfect map. (See Exercise 7 of \$31.)

(a) Show that if Y is paracompact, so is X.[Hint: If A is an open covering of X, find a locally finite open covering of Y by sets B such that $p ^ { - 1 } ( B )$ can be covered by finitely many elements of A; then intersect $\pmb { p } ^ { - 1 } ( \pmb { B } )$ with these elements of A.]

(b) Show that if X is a paracompact Hausdorff space,then so is Y.[Hint: If B is a locally finite closed covering of X,then $\{ p ( B ) ~ | ~ B \in { \mathcal { B } } \}$ is a locally finite closed covering of Y.]

9. Let $\pmb { G }$ be a locally compact, connecied topological group Show thal G is paracompact [Hint. Let $U _ { 1 }$ be a neighborhood of e having compact closure.In general,define $U _ { n + 1 } = \bar { U } _ { n } \cdot U _ { 1 }$ . Show the union of the sets $\bar { U } _ { n }$ is both open and closed in G.J

This result holds without assuming G is connected,butthe proof req uires more effort.

10. Theorem.If X is a Hausdorff space that is locally compact and paracompact, then each component of X has a countable basis.

Proof. If $\pmb { \chi } _ { 0 }$ is a component of X,then $\scriptstyle x _ { 0 }$ is locally compact and paracompact. Let C be a locally finite covering of $\scriptstyle { \pmb { \chi } } _ { 0 }$ by sets open in $\scriptstyle { \pmb { \chi } } _ { 0 }$ that have compact closures Let $U _ { 1 }$ be a nonempty element of C,and in general let $U _ { \pmb { n } }$ be the union of all elements of C that intersect $\bar { U } _ { n - 1 }$ . Show $\bar { U } _ { n }$ is compact,and the sets $U _ { n }$ cover $\pmb { \chi } _ { 0 }$

## \$42 The Smirnov Metrization Theorem

The Nagata-Smurnov metrization theorem gives one set of necessary and sufficient conditions for metrizability of a space In this section we prove a theorem that gives another such set of conditions. It is a corollary of the Nagata-Smirnov theorem and was first proved by Smirnov.

Definition.A space X is locally metrizable if every point x of X has a neighborhood U that is metrizable in the subspace topology

Theorem 42.1 (Smirnov metrization theorem). A space X is metrzable if and onlyif it is a paracompact Hausdorff space that is locallymetrizable.

Proof.Suppose that X is metrizable.Then X is locally metrizable; it is also paracompact, by Theorem 41 4.

Conversely,suppose that X is a paracompact Hausdorff space that is locally metrizable.We shall show that X has a basis that is countably locally finite.Since X is regular, it will then follow from the Nagata-Smirnov theorem that X is metrizable.

The proof is an adaptation of the last part of the proof of Theorem 40.3.Cover X by open sets that are metrizable;then choose a locally finite open refine ment C of this covering that covers X.Each element C of C is metrizable; let the furiction $d _ { C }$ ： $C \times C \to \mathbb { R }$ be a metric that gives the topology of C.Given $x \in C$ , let $B _ { C } ( { \pmb x } , { \pmb \epsilon } )$ denote the set of all points y of C such that $d _ { C } ( x , y ) < \epsilon$ .Being open in $c$ ,the set $B _ { C } ( { \pmb x } , { \pmb \epsilon } )$ is also open in X.

Given $m \in \mathbb { Z } _ { + }$ ,let $\star _ { m }$ be the covering of X by all these open balls of radius $1 / m$ that is, let

$$
\begin{array} { r } { \mathcal { A } _ { m } = \{ B _ { C } ( x , 1 / m ) \mid x \in C \mathrm { ~ a n d ~ } C \in \mathcal { C } \} . } \end{array}
$$

Let $\mathcal { D } _ { m }$ be a locally finite open refinement of $\star _ { m }$ that covers X (Here we use paracompactness.) Let $\pmb { \mathcal { D } }$ be the union of the collections $\mathcal { D } _ { m }$ .Then D is countably locally finite.We assert that D is a basis for X;our theorem follows

Let x be a point of X and let U be a neighborhood of x. We seek to find an element $D$ of D such that $x \in D \subset U$ .Now x belongs to only finitely many elements of C, say to $C _ { 1 } , . . , C _ { k }$ Then $U \cap C _ { i }$ is a neighborhood of x in the set $C _ { t }$ ,so there is an $\epsilon _ { i } > 0$ such that

$$
B _ { C _ { t } } ( x , \epsilon ) \subset ( U \cap C _ { i } ) .
$$

Choose m so that $2 / m < \operatorname* { m i n } \{ \epsilon _ { 1 } , . . . , \epsilon _ { k } \}$ .Because the collection $\mathcal { D } _ { m }$ covers X,there must be an element D of $\mathcal { D } _ { m }$ containing x.Because ${ \mathcal { D } } _ { m }$ refines $\star _ { m }$ ,there must be an element $B c ( y , 1 / m )$ of $\mathbf { \mathcal { A } } _ { m }$ ,for some $C \in \mathcal { C }$ and some $y \in C$ ,that contains $\pmb { D }$ Because

$$
x \in D \subset B _ { C } ( y , 1 / m ) ,
$$

the point x belongs to C,so that C must be one of the sets $C _ { 1 } , ~ , C _ { k }$ .Say $C = C _ { i }$ Since $B _ { C } ( y , 1 / m )$ has diameter at most $2 / m < \epsilon _ { t }$ ,it follows that

$$
x \in D \subset B _ { C _ { i } } ( y , 1 / m ) \subset B _ { C _ { i } } ( x , \epsilon _ { i } ) \subset U ,
$$

as desired.

## Exercises

1. Compare Theorem 42.1 with Exercises 7 and 8 of \$34.

2.(a)Show that for each ${ \pmb x } \in \pmb S _ { \Omega }$ , the section of ${ \pmb S } _ { \Omega }$ by x has a countable basis and hence is metrizable.

(b） Conclude that $\pmb { S } _ { \Omega }$ is not paracompact.