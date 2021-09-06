# intro
- what: building a formal functional model for the transformation A, the aritist, in terms of what constraints it has)
  - a categorical model of visualization transformations at provides a language for specifying how to specify what structure visualization library components should preserve & a functional model of how these constraints can be enforced in a library architecture. 

- why? needed a way to specify what properties and structure a visualization library architecture needed to preserve, in a way where the data model was generalizable and the graphics could be fully specifiable
  - not break data, not break graphical design, bookkeeping structure
  - Matplotlib's make anything you want - what does it mean to make anything you want and it still be a visualization?
  - solving the problem of graphic specs, not graphical design [Mackinlay],  graphical design is about specifying how the viz gets transformed into a graphic, this work is on what does it mean to implement those transformations correctly 
  - category theory let's us tear apart what are the core transformations & objects are that the library is responsible for   
  - making it functional fallows from category theory, let's us drill down to what state is actually needed by the library to do its thing - less state, easier to make parallel and more modular and all that jazz
    - How & why functional 
    - therefore is for library developers (people writing visualization libraries, not people using them)

# background
- Continuity
  - fig: matrix <- `[[lines] [image]]` (need?) 
  - continuity - what is it, why do we care
  - Butler: what are fiber bundles & why do they matter
    - local to global, bookkeeping
    - what data is needed for any part of a visual transform
  - Munzner: bookkeeping, metadata, 
  - how do visualization libraries tackle it 
    - assuming continuity:  Heer & Agrawal
      -  ggplot, networkx, imagej, etc
    - matching API to data type, Troy & Mueller,
      -  VTK, D3, Matplotlib here
   - contribution: 
     - language exxpressing continuity 
     - functional architeure for visualization libraries based on a data model which most continuities can generalize to 

- Equivariance
  - fig: commutative image that rifs on the one in K&S?
    - [[same matrix as above]] -> [[image]]
    - [[rotate matrix]] -> [[image]]
    - if I can get an example that currently fails in matplotlib, that'll show need 
  - what is it? 
    - APT, tufte, schiedigger & kindlman, 
  - how do vizualization libraries tackle it?
    - in the graphical design layer
      - APT, GoG, Vega 
  - contribution: 
    - language for expressing equivariance that architecture must ensure is preserved
    - functional architecture that allows for keeping visual transformations applied to variables consistent across visualizations (nus can be bound to fibers)
  
- category theory 
  - Vickers = intro to category theory for viz
    - is at graphical design level, but is intro
  - Easterbrook - enforcing software constraints with 
  - what does somebody reading this paper need to know about cat theory
    - objects/morphisms
    - functors
    - natural transformations  
- category theory
  - contribution: use category theory to enforce constraints in viz architecture

# TEAM
- framing? developing the language for preserving structure, how do we encode that structure?
  - first describe the domain/codamain, then the functions
    Schiedigger's 3 stages, D, V, R -> E V H
## Fiber Bundles

### Data bundle
- fig: fiber over topology w/ section w/ sample data
  - scatter w/3D fiber -[temp, pres, station] 
  - line w/ 2D fiber - [time, temp]
  - image w/ 3D fiber - [lat, lon, val]
  - network? - # fiber here might be too complicated
- continuity: K
- equivariance: F
- specified/structured data: tau
    - sheafs for gluing taus together
### Graphic bundle
- fig: graphic (scatter) in H w/ lookup over s back to rho down to screen -> possibly in Appendix w/ details 
  - continuity: S 
  - equivariance: D
  - graphic: rho

## Artist
fig: object process figure, but maybe labeled?
    - [E: Data] -nu: encode variables> [V: Visual] -q: assemble into glyph> [G: Graphic]
- broad intro of artist as function that takes Data Bundle as input, outputs graphic bundle
    - A(E) -> H 
- visual bundle V 
- equivariance:
- nu
  - fig: math diagram  [tau to mu boxes]
  - fig: [monoidal nu figure of some start, maybe still weather states ]
- q 
  - fig: math diagram pulled out to H (w/o k or S)
  - fig 2: revisit box equivariance diagram [data->q, data2->q2] 
  
- continuity: xi
  - fig: math diagram E<-H for multiple topologies, max 3 data points 
  
Appendix: q_hat
  - fig: V<-V* in middle of E to H (maybe appendix)

- end w/ big equation E->V->H, K<-S
  
## combining artists  
- why: fig [nice harmonized figure, disjointed artists]
- union
- inclusion
- & we will do more w/ this in future work

- drop equivalance altogether since we don't do anything w/ it?

# case studies: 
- intro: what is an artist in code? what's it role, why do libraries care, etc... 
  - specifically what problem in Matplotlib w/ the artist do we care to solve?
- specifying nus
- graphic/rho/Bar
  - trivial extensibility: BarH.qhat 
- fold in the data w/ look back
  - WrapperApi- maybe appendix?
- GenericArtistDraw:
  - how does this all get put together
  - parallelism/looping
- flexiblity: decouple container from topology
  - LineArtist
  - function vs. table 

# discussion
-  focus on the payoffs of this work, how the things discussed yield maintainability, extendability, scaling, & concurrency, as reviewers said the practical payoffs
  
### limitations
- reviewer suggestion of move all the math caveats here & frame this section as limitations of the math
  
### future work
- take this from the proposal since that's a scaffolded walk through of where to go w/ this model 

# conclusion
- center on main themes: continuity, equivariance, maintainability, extensibility, scaling, concurrency