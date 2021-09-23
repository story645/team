pi: E\rightarrow K
tau: K \rightarrow E

for foundation:
\tau: K (type) \rightarow E(type)

fibration (generalization) of fiber bundles which is generalizatuion of trivial bundle -> E = F \times K , trivial is map from E to F, 

trivial bundle - globally defined map from E to F, 

category theory: product: thing + arrows away from it, sum: thing + arrows go in 

tau: K \rightarrow F (function), (is key value construction)


Hom(K,F) \rightarrow f Hom(K, F') -> structure preserving operation , push forward

meters for type F, inchs for type F', f is meters to inches, you keep the K

K'\rightarrow g K \rightarrow \tau F
g*\tau = \tau \circ g: K' \rightarrow F

Hom(K, F) \rightarrow g* Hom(K prime, F): K'= U \subset K, example g is restriction

if we have F w/ scale and translations or rotations or other allowed F, talking about how they act on functions, how that transforms, map it to visualizations, 
morphisms need to be preserved through to visualizations

one object category is a monoid

equivariance is that a monoid is preserved /all the diagrams would commute 

catagory w/ data bundles 

wrong: E->E'

special class of decators that only modify ootput or input
    - pair(g,f) are restricted decorators on bundles
    - takes functions to functions and sections to sections

nu is a postcompose bundle map (don't touch K)
    - post compose is a covariant
    - operation on outputs
xi is a precompose bundle map
    - operation on args

category theory is basically "equivariant by definition"


some transformations will just push forwards (scale, color, etc)

ex: change hatch density -> Q is not equivariant on bundle level at like change hatch density cause no map on the bundle - Hatch density is a parameter of rho

for some variables, Q is like nu and can demand equivariance, but not when we need to change the rho - then we push the equivariance down to the rho

can be made equivariant on ImQ if property of Q holds

double check def of full subcategory
- full subcategory of data bundles
  - consists of continous maps/continous transformations of keys, fiberwise maps
  - nu knows how to take fibers to fibers: F to P, postcomposes, can do chained nu
  - precomposing w/ nu if it's still over K


whichever categories that you're allowing, maps include continous maps on subspaces, any map from bundle to bundles , restricts to structure preserving maps on the bundle, once define the fiber then other category is determined, those are not allowed, this subcategory is defined, input type is objects, output type is objects, what are these objects? 
functor maps objects in one category to objects in other category, objects may not be sets, elements of these objects are sections

A(\Gamma(K,E)) = \Gamma(S,H)
C \rightarrow A D

{* \in c}}\rightarrow h K, h*E = F, \tau*K = tau(k)  \in F)k

diagram where S->K, which gives what rho corresponds to tau (with point inclusions)

b/c you can map points, you can map sections to S
allowed:K and subset K

category of subsets w. inclusions. etc..

continuity is cause continuous maps

%%- brief intro to artist in most simple form $\vartist \dtotal \rightarrow \gtotal$ 
%% flesh out categorical framing of artist, walk through how eq 16 is part of implementing the artists
%% https://github.com/story645/proposal/blob/main/notes/meetings/2021_08_30.md

%% domain of A is category E, with sheaves on E7   
%% range of A is category H, sheaves on H
%% category bundles, functions are bundles maps, 
%% subset/restriction is a type of bundle map - bundle over subset is bundle over whole thing, which induces map on section which goes other way which is restriction
%% bundle map induces a sheaf map, fibers themselves are categories, map from fiber to fiber that's legit in F
%%% what is the set up? category of bundles, bundle maps - fiber have some structure/any structure/no structure - bundle maps should be functors, A is gonna be a functor, H is a category of bundles + sheaves of bundles, A is a functor
%%% we claim that for visualizations, A decomposes as 
%%% nu bundle map on bundle + functor on fibers, Q takes you to H
%%% K to S is pullback of deform retract, A is functor on imageA in H


1) bundle E restricted to U is presheaf, 

F_1: \mathcal{K_1} \rightarrow Set <-presheaf is the functor F_1
any map on base spaces will give us a map on functors, sections will pull back

artist w. particular base space w/ particular, 

How do you define the category E
objects: F_1 
  - presheaf: is it defined on fixed K and E0 (this provides the Equivariance on fibers + continuity), declaring it as E->V is natural transformation
  - presheaves: is it defined on arbitrary K and Eo
morphisms: inclusion -> these go back and forth, hence is a profunctor

fiber preserving maps 
fiber as category -> map preserves the structure, monotonic etc

How are you defining the artist? fix E0 and K and nu and q

same sheaf w/ arrow to itself , requires that all bundles be morphisms of a bundle to itself
  - morphisms are actions, bundle to bundle which when restricted to bundle are morphisms of bundle to itself 

- presheaf is just a functor

F is object in category that just has itself as only object 
if we have a bundle transfrom F_0 to F_0, then we have a natural transfrom F_0 to F_0

same thing has to happen on V side, declare which bundle maps are OK on which side, nu goes from one to the other, preserving the structure3 , doesn't have to have the same dimension,
- we don't care about a change in fiber dim - nu defines type it eats, which is static and defined relative to the fibers - can't change K, or E, nu is fixed on F/E, V and E can be different dimensions

category w/ one functor E_0, morphisms are functor to itself, f is data to data, g is graphic to graphic, nu(f) \rightarrow (g), when we get to H bundle, 
V over K -> H over S, 

nu is bundle to bundle (natural transformation)
Q is a natural transformation - proposition, map that satisifies this condition, v \rightarrow h v, 
