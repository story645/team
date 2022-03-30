### Types


- category C
- morphisms in category theory are $f: obj_1 -> obj_2, obj_1, obj_2 \in Obj(C)$

category theory objects is a class in programming 
- morphisms are methods between instances of different classes 
- categories are metaclasses 


#### Topological Base Space Class
- K: topological space, objects are points in space
- $(K, \tau)$ topology on K, sets of open sets

class: points in topoligical space 
Artist is designed to work on points k
- A((point_on_circle-> fiber))
    - can encode as set of transition functions? 
    - bundle is points + transition functions
- implement as simplacial complex? 
- rotation of 10 degrees 
- 
#### Sets
- objects: sets of sections, e.g. $\Gamma(U, E|_U)$
    - programming: class for each type of section
    - class Tau, object tau which is really a function 
    - class Mu, class Rho
    
$A: \Gamma(U, E|_U) \rightarrow \Gamma(W, H|_W)$
$\nu: \Gamma(U, E|_U) \righatrrow \Gamma(U, V|_U)$
$\Q: \Gamma(U, V|_U) \rightarrow \Gamma(W, H_W)$

#### Fiber
- classes: arbitrary types 
    - methods: $\widetilde\phi: F \rightarrow F$
- can build up: $\otimes: F \times F \rightarrow F$

#### Total Spaces:
- Data: $(E, \pi, F, K)$
- Visual: $(V, \pi, P, K)$
- Graphic: $(H, \pi, D, S)$

### Functions:

#### Sections
- $\tau: k \mapsto F_k$ 
    - $(K \rightarrow F)$
- $\mu: k \mapsto V_k$
    - $(K \rightarrow V)$
- $\rho: s \mapsto D_s$
    - $(S \rightarrow D)$
##### constraints:
-- sections of sheaves, so can be glued together over intersections or localized to small regions (indexes)

- sections on decomposable fiber spaces are decomposable (field selection)
     - $\tau \in Hom(K, F_1 \times F_2) = \tau_1 \in Hom(K, F_1) \times tau_2 \in Hom(K, F_2)$
    - start with if F decomposable then... 
        - the pieces that still make sense at the level of the bundle 
            - speed - (N|S, E/W) can be broken up at fiber level not at bundle level
                - transition function will break on individuals 
        - decomposable up to preservation by transition functions

#### Artist
- $A: \tau \mapsto \rho$
    - $(k \rightarrow F_k) \rightarrow (s \rightarrow D|_s), \xi(s)=k$
    - $A(\Gamma(K, E|_K)) = \Gamma(S, H|_S))$
- $\xi: s \rightarrow k \;\forall s \in S$

- $\xi: \S \rightarrow K$
- deform retract
- $\xi_*$ screen to data
- $\xi^*$ data to screen 

#### Composition
- $\bigsqcup A_i(\Gamma(K_i, E_i|_{K_i})) = A(\bigsqcup \Gamma(K_i, E_i|_{K_i}))$ b\c $\bigsqcup \Gamma(S_i, H|_{S_i}) = \Gamma(\sqcup S_i, H|_{\sqcup S_i})$


#### constraints:
- $\eta(\tau) = \delta(A(\tau))$ expected measurement = actual measurement
- $\eta(\phi\tau) = \phi(\delta(A(\tau))$ -> change in data reflected in change in measurement
    - ways to deconstruct this if we don't have data/only image + expected change in measurements - see slides
- continuity constraint

#### Artist Decomposition
## $\nu$
- $\nu: \tau \mapsto \mu$
    - $(K \rightarrow E) -> (K \rightarrow V), V:=E$
- $\otimes: \nu_x\times \nu_y  \rightarrow \nu_scatter$
- $\nu^bar = \nu^rectangle_patch \circ \nu^scatter$
+ equivariance $\widetilde\phi$

## Q
- $Q: \mu \mapsto \rho$
    - $(K \rightarrow V) \rightarrow (S \rightarrow H)$
    -  $\bigsqcup Q_i(\Gamma(K_i, E_i|_{K_i})) = Q(\bigsqcup \Gamma(K_i, E_i|_{K_i}))$ b\c $\bigsqcup \Gamma(S_i, H|_{S_i}) = \Gamma(\sqcup S_i, H|_{\sqcup S_i})$

- $A = Q \circ \nu$, $A_1 = Q_1 \circ \nu_1, A_2 = Q_2 \circ \nu_2, A_1 = A_2$