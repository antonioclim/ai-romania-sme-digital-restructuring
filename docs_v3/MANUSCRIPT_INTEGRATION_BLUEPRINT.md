# Information & Management manuscript integration blueprint

## Status

This is a controlled integration blueprint, not a submission-ready manuscript.
No simulation result from CI is to be transferred into the article. No
independent replication is claimed before a real dataset has been selected,
audited and analysed.

## 1. Working article identity

### Preferred methodological title

**Outcome-Definition Sensitivity Analysis: Auditing categorical outcomes in
Information Systems research**

### Reserve title

**When binary adoption measures change the phenomenon: Outcome-Definition
Sensitivity Analysis for Information Systems research**

The final title remains open until the literature-collision audit is complete.

### Central claim

Categorical outcome construction can alter not only a reported level but the
composition, association pattern, subgroup order and set of claims that remain
defensible. ODSA makes those consequences explicit without presuming that
alternative definitions estimate one unchanged construct.

## 2. Target contribution architecture

The article must make three distinct contributions.

### Conceptual contribution

Separate legitimate outcome broadening from engagement-state conflation.
Broadening is not intrinsically invalid. The inferential error occurs when a
broad positive class is narrated as evidence of a narrower state that some
positive cases do not satisfy.

### Method contribution

Formalise ODSA as a non-scalar audit comprising:

- state registration;
- definition relations;
- exact level decomposition;
- positive-class composition;
- association contrast;
- subgroup-order sensitivity;
- conservative claim admissibility.

### Evidence contribution

Demonstrate the method through:

1. controlled simulation;
2. the Romanian organisational AI worked application;
3. an independent Information Systems replication.

The Romanian response set cannot carry the validation burden alone.

## 3. Provisional section structure

1. **Introduction**
   - outcome construction as an IS inference problem;
   - why alternative definitions may change the phenomenon;
   - gap relative to construct validity and analytical-sensitivity methods;
   - three contributions.

2. **Conceptual foundations**
   - categorical states and construct–indicator–inference alignment;
   - adoption, implementation, assimilation and use;
   - multiverse, specification curve and measurement-practice boundaries;
   - outcome broadening versus engagement-state conflation.

3. **Outcome-Definition Sensitivity Analysis**
   - notation and assumptions;
   - diagnostics;
   - propositions and counterexamples;
   - six-step protocol;
   - boundary conditions.

4. **Simulation study**
   - prespecified mechanisms;
   - generating, sampled true and observed layers;
   - factorial design;
   - results;
   - implications for method use.

5. **Study 1: organisational AI engagement**
   - design and evidence ceiling;
   - state and definition register;
   - levels, composition, association and claim admissibility;
   - sensitivity to possible duplicate units and coarsening, where feasible.

6. **Study 2: independent IS replication**
   - dataset provenance and licence;
   - construct-specific state register;
   - replication results;
   - cross-study comparison without forced equivalence.

7. **General discussion**
   - theoretical contribution to IS measurement;
   - complementarity with adjacent methods;
   - implications for KPI governance and cross-study comparison;
   - boundary conditions;
   - research agenda.

8. **Conclusion**

## 4. Journal-facing method kernel

> We define an observed state space \(S=\{s_1,\ldots,s_K\}\) and represent each
> categorical outcome definition as a non-empty subset \(d\subseteq S\). The
> resulting binary outcome is \(Y_i(d)=\mathbb{1}(s_i\in d)\). ODSA does not
> assume that alternative definitions estimate the same construct. It first
> registers their set relation and intended question, then evaluates five
> separate dimensions: level, positive-state composition, association with a
> prespecified descriptor, subgroup-order stability and claim admissibility.
> For nested definitions, level is monotone by construction. Association and
> subgroup order are not. For non-nested definitions, the level contrast is
> decomposed into states added by one definition and states removed by the
> other.

> Claim admissibility is deliberately conservative. A claim \(q\) identifies
> the set of observed states compatible with its wording, \(S_q\). Definition
> \(d\) is admissible only when \(d\subseteq S_q\). This condition prevents a
> broad positive class from being interpreted as evidence of a narrower state,
> but it does not establish construct validity, causal identification or
> external generalisability.

## 5. Planned tables

1. ODSA compared with adjacent methods.
2. Notation, diagnostic and inferential boundary.
3. Formal properties and practical consequences.
4. Simulation factors and controlled mechanisms.
5. Simulation primary results.
6. Romanian application: levels, composition, association and claims.
7. Independent replication.

## 6. Planned figures

1. State register → definitions → diagnostics → admissible claims.
2. Definition graph and symmetric-difference decomposition.
3. Counterexamples for association and subgroup-order non-monotonicity.
4. Simulation sensitivity map.
5. Romanian worked application.
6. Independent replication.

## 7. Claims unavailable at this stage

Do not write that:

- the full simulation has validated ODSA;
- ODSA outperforms specification curve analysis;
- ODSA improves managerial decisions;
- the Romanian response set represents Romanian SMEs;
- Study 2 exists;
- the ethics gate is closed;
- `v3.0.0` or a new DOI exists.

## 8. Word-budget principle

A working target of approximately 9,000–10,500 words may be defensible, subject
to the live journal guide at submission. The formal framework and simulation
must receive more space than the Romanian application. The result must not
look like the previous TASM article with a simulation appendix attached.

## 9. Integration gate

Manuscript rewriting may begin only after:

- the formal properties pass executable tests;
- the novelty boundary survives the dedicated literature audit;
- the full simulation protocol is frozen;
- Study 2 is selected and licensed;
- the ethics statement is factually supportable.
