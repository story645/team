1. pullback - restriction: iota is restriction 
2. clean up $K^{op}$ definition
3. rename f:E\rightarrow E to different letter
4. image of a sheaf is a sheaf, is not a category, is a contravariant functor, write words about what Im_A is 
5. eq 8:  not all \Gamma(U,H) is reachable from imA, only a subset of \Gamma(U,H ) reachable via A, sheaf im_A is im_A: S^{op} to \textit{Set}, subcategory im_A - collection of subsets of sets in P -> for \Gamma object in P, subset of that \Gamma is in imQ, 
6. rename (5) to an association rather than a function? notation for morphism of functors
7.  ditch the tau category altogether, rewrite graphics paragraph w/o P
8.  ditch (8) 

# artist composition: 
1. how do we express that we're intending b and not a? 
2. operations are restrictions on ranges 
3. map x to vv, identifying x via projections to induce same transform -> factor through x3 
### artist composition
1. disjoint union of unlike things
2. base space inclusions -> inclusion maps are on S too
3. fiber projections over one point -> sum w/ understanding to be linked, for d to commute they have to have consistent inclusion - fibers keep projecting up, concatenating columns, -> tuple keeps going up 

# K & S 
## stages
### data D: 
- TEAM: \mathcal{E}
- the underlying mathematical structure of the data or object being visualized,
  - mathematical types of the individual data points
  - organization of the data points
  - operational context
  - actions (but they don't call it this)
    - linear transforms on the space + properties/ partial orders
    - ordering maps for trees
    - 
### representations R: 
- TEAM: implementation of \mathcal{E} + \mathcal{E}\rightarrow \mathcal{E'}
- concrete representation of the data in a computer,
  - data structure? list or table, vector 
  - computation: samples, 

### visualization V:
- TEAM: how folks view \mathcal{H}
- mathematical description of how humans perceive the visualization.

## principals
1. representation invariance
    - how data is encoded shouldn't change the viz
      - ex: numpy array | pandas dataframe -> same line plot
    - visualization should not depend on the specifics of how the underlying data is represented
    - TEAM: preserving sheaf maps in the implementation of E means those maps carry through
2. unambigous data depiction
   - changing the data should change the viz
    - data and data + 2 don't yield the same plot
   - TEAM: \varphi commutes to ImA_{\varphi}
   - Ziemkiewicz and Kosara injectivity: 
3. visual-data correspondance
    - large changes in data should yield large \varphi
    - visual affordances should match important low-level tasks
    - TEAM: \varphi commutes to ImA_{\varphi}

## notation
* symmetry: group actions; invertible transformations that when applied to each element in a set of things, map back to the same set. 
* affordances: something perceived in the environment to provide the possibility
of action (Gibson, http://cs.brown.edu/courses/cs137/2017/readings/Gibson-AFF.pdf),
