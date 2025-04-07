Most importantly, the authors do not precisely describe how they "Model the data structures that store the datasets as sheaves", which makes the transformations between these sheaves which are supposed to model visualization hard to decipher.
- [ ] link to papers (like polars maybe) that show how data containers already are implemented as sheaves. also sheaves table in appendix

- [ ] Similarly, the authors abstract ends by claiming that "Using category theory to formally express how visual elements are constructed means we can translate those expectations into code, which can then be used to enforce the expectation that a visualization tool is faithfully translating between numbers and charts," but no aspect of how the translation into code is executed nor of how expectations are enforced (presumably, some kind of verification?) is described in the paper itself.
    - [ ] verification figures/diagrams in construction section
    - [ ] the typing notation in the paper
    - [ ] clean up discussion example
---

Comments and questions

- [ ] What is a "line algorithm"?
    - [ ] change to line drawing
    - [ ] add citation for line drawing algorithim,

What does it mean for "continuities" to be "homeomorphic"? It seems to me that your intended meaning of the term "homeomorphic" is weaker than the conventional definition in topology. You say in Figure 3 that asking for a transformation to be "homeomorphic" means that "there exists a deformation retract ξ : S → K between graphic and artist base space". A deformation retract is an instance of a homotopy equivalence; should you be using "homotopic" in place of "homeomorphic"?
- [ ] definition of homemorphism we're using is in related work, key is the continuos inverse
    - [ ] stress homeomorphism > homotopy b/c of Kosara/Z readability (every glyph must map back to data)
- [ ] add homeomorphism conditions to $\xi$ (w/ notion of choosing topology K s.t.  homemorphism exists)

You introduction ends by stating that your method is improves on some other cited methods "by explicitly incorporating topology" and "by providing a framework for translating the theoretical ideas into buildable components". Taking a cursory sample of the references provided, Wilkinson's book has an entire chapter (13, "Space") on the topological structure of data, while Mackinlay's paper claims to implement an AI based tool. In other words, your citations rather undermine your claimed advantages, and you should be making a more explicit comparison between your treatment and theirs.
- [ ] "by explicitly incorporating topology"
    - [ ] add a sentence or two to related work topology talking about how "topology" all follows the mark match implantation model and here we introduce a generalized formalism of the implicit expectation
        - [ ] add sentence on Wilkonson chap 13: He discusses mathematical spaces, but explicitly won't generalize b/c
            - [ ] " . Restricting ourselves to homeomorphic mappings would eliminate many useful charts, the most obvious being planar geographic maps" <- our framework doesn't need that restriction b/c the generalization to non-trivial bundles accounts for it
            - [ ] instead he embeds in a metric space/other - figure out if metric space distance functions are $\hat{phi}$ in a presheaf context
                - maybe: https://arxiv.org/abs/1901.09077
- [ ] "by providing a framework for translating the theoretical ideas into buildable components"
    - [ ] make clear that this is a contribution of this work but not the novelty
    - [ ] contextualize in terms of the software related work - topology independent (where as existing very structure driven)
- [ ] answer to both is make clear that the improvement is in the generalization

- [ ] You also mention "supporting non-group and non-monoidal structures", but since you do not mention these terms again, let alone any examples of data structures that lack these structures that your framework is thus able to treat in contrast to the cited ones, it is unclear what advantage is being claimed there.
    - [ ] related work section goes into depth about
    - [ ] emphasize that the equivariance diagram shows binning, which is a monoid not a group
    - [ ] change to "encapsulate/generalize"

- [ ] Comparing Figure 2 with Table 1, it seems that the former is supposed to illustrate the final column of the latter, but if so where is the total space $H$ in Figure 2?
    - [ ] add note that figure 2 is assuming a trivial bundle H = $D \times S$ and figure is illustrating the section map $S->D$ (b/c showing the total space is too weird)

- [ ] In "The indexing space is modeled as a topology ... because it is a uniform method of describing arbitrary continuity and it provides a method for managing overlapping embedded topologies", what is "it"? If "it" just refers to the use of topology, putting aside the circularity (perhaps you meant "topology" in two different senses in this sentence..?) you don't need to convince mathematicians that topology can formalize notions of continuity, but considering that you are eventually supposed "translate the theoretical ideas into buildable components", you will need to consider at some stage how the topologies involved can actually be modelled computationally.
    - [ ] it -> modeling the indexing space as a topology, but really unravel this sentence
    - [ ] indexing spaces-> clarify in discussion section/ensure there's an example

- [ ] What are "domains of types"?
    - [ ] example of this in the Spivak discussion but also just use Spivak's terminalogy

- [ ] You claim that "Abstracting the data containers as sheaves provides a way of encoding how data containers keep track of the continuity of the data [5] such that visual algorithms developed on this model apply whether the data fits in memory, is distributed, or is streaming". The two halves of the claim seem disconnected: I don't doubt that sheaves can handle continuity, but that determines how the algorithm structures data after receiving it, which seems orthogonal to the question of how and where the data is stored beforehand. Perhaps your claim is rather that sheaves allow parallelism, so that not all data needs to be immediately available in order for approximations of the visual output to be produced. If so, this assertion needs to be made explicitly and supported in its own right.

- [x] At the start of Section 3, what is $\rho$? You mentioned earlier that $\tau$ is a section of a bundle (which bundle?); presumably $\rho$ is too.
    - [x] this is discussed in "Uniform abstract graphic representation" section

- [ ] Naming a mapping "artist" after a class in Matplotlib seems doubly insulting to actual visual artists and graphic designers. Given that you are happy to use mathematical notation for the other components, you need a pretty strong case for how this mapping is doing something artistic to defend the choice to name this mapping at all.
    - [ ] clarify that it's named for the part of the library architecture it's abstracting:
        - " At its highest level, the matplotlib API has three basic classes: FigureCanvasBase is the canvas onto which the scene is painted, analogous to a painter’s canvas; RendererBase is the object used to paint on the canvas, analogous to a paintbrush; and Artist is the object that knows how to use a renderer to paint on a canvas. Artist is also where most of the interesting stuff happens; basic graphics primitives such as Line2D, Polygon, and Text all derive from this base class."
        - artist is what translates the data (real world) into the instructions for drawing the visual (like human artists conjure images based on ideas/prompts/directives/etc and then their arms draw)

I have many questions about the contents of Figure 3.
- [ ] How is the stated 'homeomorphic' condition related to naturality?
    - Harder's lectures - homemorphic map between base spaces means pullback/pushforward means exists natural transform
- [ ] What is $Dir^{\alpha}(k)$?
    - make sure to explain that example is showing the dirchilet distribution and why
- [ ] What are $\hat{\phi}$ and $\tilde{\phi}$ and what do the subscripts on them refer to; if the subscripts are total spaces from Table 1, why is the codomain of $\hat{\phi}_E$ labelled with the same letter as the base space?
    - [ ] make each of them a definition in the respective sections
    - [ ] add a note about how subscripts are for the side {date, viz} the transform is on (and change hat subscripts to base space)
- What does the prime in $K'$ and $S'$ refer to? Are there in fact supposed to be several of each kind of bundle around?
    - [ ] make clear that these are base spaces and these shouldn't actually be K'/S' b/c they're the same type as K/still K (same w/ the little k/k')
- What is the rotation in the triangle supposed to illustrate, and in what way is the transformation of the visual on the right-hand side relate to $\phi$?
    - [ ] part of figure explaination - rotation on the base space/rotated figure

- The caption of Figure 4 only explains a small fraction of what is happening in the diagram. In particular, it is unclear which side of the diagram is supposed to be "data" and which "visualization", both sides containing data (a table and a list of coordinates, respectively) and a visualization...
    - [ ] add a human readable title to each quadrant: graphic at point, graphic, data, data at pixel

- [ ] I don't know what it means for a topology to be "equipped with operators", or what a "record" is, although I presume you are trying to say that your framework includes a way to extend the topological spaces involved when further data is added.
    - [ ] yes
    - [ ] record is explained in fiber section/spivak section
    - [ ] figure out what the actual language is (not equipped w/ operator)
---

Typos / minor comments

- [ ] Astract: "a method for specifying visualization methods" -> maybe replace the former 'method' with another word.

- [ ] "a set of actions on a group" -> I presume the preposition should be "of"? Missing full stop.

- [ ] "Topological structure is generally assumed ... but generally do not verify that input structure" -> Does "input structure" refer to "topological structure"? The second half should be in the passive voice in that case: "...but this input structure is typically not verified."

- [ ] "encode multi-dimensional fields can be encoded" remove last three words.

- [ ] "artist base space" -> inspecting Table 1, I suppose this is supposed to be either the 'data' or the 'visual' base space?

"As illustrated in 4" -> should be 'Figure 4'.

- [ ] "how visual elements correspond to distinct data elements" -> should be 'distinct visual elements'

- [ ] "respectively, Since" -> should be '.'
