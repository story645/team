## reorder:
# inclusion & equiv can be done as O_E->O_H 
# equiv can then be used to introduce O_A which is the constraint on O_H
# bundles: 
## data: 
* $(E, K, \pi, F)$
* sections: $\{\tau: k \rightarrow r \mid k \in K, r \in F\} \coloneqq \Gamma(K, E)$
* sheaf: $\mathcal{O}_E: U \rightarrow \Gamma(U, E)$, $U \subset K$

## visual?:
* $(V, K, \pi, P)$
* sections: $\{\mu: k \rightarrow p \mid k \in K, p \in P\} \coloneqq \Gamma(K, V)$
* sheaf: $\mathcal{O}_V: U \rightarrow \Gamma(U, V)$, $U \subset K$

## graphic
* $(H, S, \pi, D)$
* sections: $\{\rho: (s_x, s_y) \rightarrow d \mid (s_x, s_y) \in S, d \in D\} \coloneqq \Gamma(S, H)$
* sheaf all: $\mathcal{O}_H: W \rightarrow \Gamma(W, H)$, $W \subset S$
* reachable sheaf: $\mathcal{O}_A: W \rightarrow A(\mathcal{O}_E)$


## Artist

* morphism: $S \xrightarrow{\xi} K$, $U \subset K, W \subset S$
* $\mathcal{O}_E: U \rightarrow \{\tau: k \rightarrow r \mid k \in K, r \in F\}$, $k \in U \subset K$
* $\mathcal{O}_A: W \rightarrow \{\rho: s \rightarrow d \mid \rho(s) \in A(\tau(k)), \tau \in \mathcal{O}_E, \xi(s)=k\}$
* NOTE: $\mathcal{O}_{A}$ is defined circularly

### sheaf pullback/pushforwards
* morphism: $S \xrightarrow{\xi} K$
* pushforward $\mathcal{O}_A(S) \xrightarrow{ \xi_*} (\xi_*\mathcal{O}_A)(K)$
  
    $\{\rho: s \rightarrow d \mid s \in S, d \in D\} \xrightarrow{\xi_*} \{\rho: \xi^{-1}[k] \rightarrow d \mid \xi^{-1}(k)\subset S\}$  

* pullback: $(\xi^*\mathcal{O}_E)(S) \xrightarrow{\xi^*} \mathcal{O}_E(K)\}$
  
    $\{\tau: \xi(s) \rightarrow r \mid \xi(s) \in K, r \in F\}\xrightarrow{\xi^*}\{\tau: \xi \rightarrow r \mid k \in K, r \in F\}$

    ![](figures/pushpull.png)