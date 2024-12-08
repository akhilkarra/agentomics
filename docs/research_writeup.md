# Agentomics: Simulating Macroeconomic Dynamics with Intelligent Agents

Author: Akhil Karra \
*Undergraduate 3rd-Year Student at Carnegie Mellon University studying Mathematics, with a concentration in Statistics, and AI.*

```{contents}
:depth: 2
```

## Introduction

Understanding macroeconomic systems requires dissecting complex interactions among financial institutions, regulatory bodies, and market forces. These interactions, shaped by decisions of interdependent agents, present a challenge for researchers seeking to model and analyze emergent behaviors within such systems. Traditional approaches, such as rule-based models or game theory, often struggle to capture the dynamic and heterogeneous nature of these interactions (de Zarzà et al., 2023).

Recent advancements in Artificial Intelligence (AI), particularly Large Language Models (LLMs), have introduced new possibilities for modeling multi-agent systems (MASs). LLMs provide agents with advanced reasoning capabilities, enabling them to process nuanced inputs, adapt to changing environments, and communicate effectively. This has opened the door to innovative research on LLM-powered MASs, including their applications in decision-making (Huang et al., 2024) and macroeconomic simulations (Li et al., 2023).

Building on these developments, *Agentomics* is an exploratory project that leverages the Langroid framework to simulate macroeconomic systems using intelligent agents. By integrating economic principles with cutting-edge AI, *Agentomics* investigates how agent interactions—representing banks, regulators, and the broader economy—can provide insights into financial stability and the ripple effects of policy decisions.

This project also reflects a personal journey of learning. Much of the work involved understanding MASs, becoming proficient with Langroid, and designing agent behaviors to align with macroeconomic concepts. The economic insights gained, though preliminary, highlight the potential of combining MASs and LLMs for studying complex systems.


## Project Methodology

The *Agentomics* project focuses on modeling macroeconomic dynamics through a simulation involving four distinct types of agents. Each agent is designed to reflect a specific role within the financial ecosystem, leveraging LLMs to make decisions, adjust economic variables, and interact with one another dynamically.

### Agent Design and Roles

1. **SmallBank**: Represents community-focused financial institutions. These agents simulate grassroots behaviors like localized lending and borrowing, highlighting their influence on regional economies.
2. **BigBank**: A proxy for large commercial banks with national or international reach. These agents manage large-scale lending operations, adjust reserve requirements, and interact heavily with regulatory policies.
3. **CentralBank**: Models regulatory authorities responsible for monetary policy. It executes actions such as adjusting interest rates and implementing quantitative easing to maintain economic stability.
4. **EconomyAgent**: The central orchestrator of the simulation. This agent aggregates inputs and feedback from all others, ensuring the simulation’s cohesiveness and alignment with real-world economic dynamics.

Each agent’s behavior is powered by LLMs configured using Langroid’s flexible architecture. The decision-making process incorporates contextual inputs, historical data, and economic theory.

### Simulation Environment

The simulation operates as a closed-loop system where agents communicate and interact based on defined parameters, or "knobs." Examples include:
- **Interest Rates**: Adjusted by the CentralBank agent to influence borrowing and lending activities.
- **Lending Policies**: Controlled by SmallBank and BigBank agents to reflect their operational priorities.
- **Macroeconomic Indicators**: Monitored and adjusted by the EconomyAgent to guide overall dynamics.

Interactions are facilitated by Langroid’s messaging framework, which enables agents to share information, negotiate, and respond to changes in their environment. This architecture mimics real-world economic behaviors, providing a robust platform for exploration.

<!-- ### Challenges and Learning

Much of the project’s initial focus was on mastering the tools and frameworks required for implementation:
- **Langroid Integration**: Understanding how to utilize Langroid for agent-based modeling and ensuring seamless communication between agents.
- **Agent Design**: Balancing the complexity of agent behaviors with the constraints of LLMs, such as context limitations and response consistency.
- **Simulation Refinement**: Iteratively testing and tuning economic parameters to produce realistic outputs.

These efforts laid the groundwork for deriving meaningful insights and demonstrated the feasibility of applying LLMs and MASs to macroeconomic research. -->

## Economic Takeaways



## Lessons Learned

While creating and running the simulations, I gained some valuable insights into the challenges and best practices of designing LLM-powered multi-agent systems (MASs). Two key lessons emerged from integrating Langroid and running simulations:

### Ensuring Sensible Outputs
One major challenge was ensuring that agent outputs were not only valid but also meaningful for the simulation. For instance, the `CentralBank` agent’s percent change in securities holdings had to represent a true percentage, not an absolute value. While Langroid supports basic type assertions (e.g., `int` or `float`), more granular checks were necessary for this use case.

To address this, I developed custom types like `Percent` and `NonnegPercent`, which validate percentage values during initialization. Additionally, I created a `TypedArray` class to dynamically type-check lists of elements as they were updated. These tools streamlined the type-checking process, ensuring accurate and consistent agent behavior during simulation runs.

### Managing LLM Bias and Output Processing
Another key lesson was the importance of reducing bias in LLM-generated responses and rigorously analyzing outputs. For example, I designed prompts to place the agents in a fictional country with no temporal context or direct references to real-world events. Despite these efforts, the LLM mentioned the COVID pandemic when backtesting the system, even though no such data was explicitly provided. This highlighted how specific input values could implicitly trigger unexpected associations and correlations in the model.

This insight underscored a critical design consideration for LLM-powered MASs: natural language outputs may not always conform to expectations and can reflect latent biases in the model. Langroid simplifies extracting structured data from LLM outputs, but additional post-processing can be necessary to ensure validity and relevance for specific use cases.

## Applications and Future Directions

This project opens several avenues for applying and extending multi-agent simulations in macroeconomics. While the project primarily focused on exploring the feasibility of integrating intelligent agents with macroeconomic principles and deriving some initial insights from the system, its potential applications are broad and impactful.

### Applications

1. **Economic Modeling**
   - By simulating interactions between banks, regulators, and the broader economy, *Agentomics* offers a framework for exploring systemic risks, financial stability, and the cascading effects of economic policies.
   - Researchers can use similar simulations to test hypotheses about macroeconomic behaviors, such as the impact of interest rate changes or lending policy adjustments.

2. **Educational Tools**
   - The project provides a hands-on, interactive environment for students and educators to explore complex economic concepts.
   - It can be adapted into classroom activities, where students experiment with different scenarios and observe the resulting macroeconomic dynamics.

3. **Policy Prototyping**
   - Policymakers can leverage MAS-based simulations to test the effects of proposed regulations in a risk-free virtual environment.
   - For example, adjustments to reserve requirements or interest rates can be studied to predict their outcomes on financial stability and market activity.

### Future Directions

1. **Expanding Agent Behaviors**
   - Future iterations could include more granular agent behaviors, such as sector-specific banks or consumer agents making microeconomic decisions like spending and saving.
   - Incorporating machine learning models for decision-making could further enhance agent realism and adaptability.

2. **Integrating Real-World Data**
   - Coupling the simulation with real-world datasets, such as historical economic indicators or financial transaction data, would provide richer insights and more accurate modeling.
   - This integration could also allow agents to make data-driven decisions, enhancing the simulation’s relevance for policy analysis.

3. **Refining LLM Utilization**
   - While the current simulation leverages LLMs effectively, exploring advanced techniques like fine-tuning or reinforcement learning could improve decision-making accuracy.
   - Testing additional LLM models with larger context windows and domain-specific training might resolve some current limitations, such as context loss or inconsistent responses.

4. **Scalability and Complexity**
   - Scaling the simulation to include larger numbers of agents and more intricate interactions could reveal emergent patterns that are otherwise obscured in smaller simulations.
   - Adding features such as multi-period forecasting or stochastic elements could enhance the realism of the economic dynamics.

5. **Cross-Disciplinary Applications**
   - Beyond macroeconomics, the framework used in *Agentomics* could be adapted for other domains where complex, interdependent systems exist, such as supply chain management, urban planning, or climate modeling.

## Conclusion



## References

1. **de Zarzà, I., de Curtò, J., Roig, G., Manzoni, P., Calafate, C. T.** (2023). Emergent Cooperation and Strategy Adaptation in Multi-Agent Systems: An Extended Coevolutionary Theory with LLMs. *Electronics*, 12(2722). https://doi.org/10.3390/electronics12122722

2. **Guo, T., Chen, X., Wang, Y., Chang, R., Pei, S., Chawla, N. V., Wiest, O., Zhang, X.** Large Language Model-based Multi-Agents: A Survey of Progress and Challenges. *arXiv.org*. https://doi.org/10.48550/arXiv.2402.01680

3. **Huang, J., Li, E. J., Lam, M. H., Liang, T., Wang, W., Yuan, Y., Jiao, W., Wang, X., Tu, Z., Lyu, M. R.** How Far Are We on the Decision-Making of LLMs? Evaluating LLMs’ Gaming Ability in Multi-Agent Environments. *arXiv.org*. https://arxiv.org/abs/2403.11807

4. **Li, N., Gao, C., Li, Y., Liao, Q.** (2023). Large Language Model-Empowered Agents for Simulating Macroeconomic Activities. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.2310.10436
