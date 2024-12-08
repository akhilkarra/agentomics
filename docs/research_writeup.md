# Agentomics: Simulating Macroeconomic Dynamics with Intelligent Agents

Author: Akhil Karra \
*Undergraduate 3rd-Year Student at Carnegie Mellon University studying Mathematics, with a concentration in Statistics, and AI.*

```{contents}
:depth: 2
```

## Introduction

Understanding macroeconomic systems requires dissecting complex interactions among financial institutions, regulatory bodies, and market forces. These interactions, shaped by decisions of interdependent agents, present a challenge for researchers seeking to model and analyze emergent behaviors within such systems. Traditional approaches, such as rule-based models or game theory, often struggle to capture the dynamic and heterogeneous nature of these interactions (de Zarzà et al., 2023).

Recent advancements in Artificial Intelligence (AI), particularly Large Language Models (LLMs), have introduced new possibilities for modeling multi-agent systems (MASs). LLMs provide agents with advanced reasoning capabilities, enabling them to process nuanced inputs, adapt to changing environments, and communicate effectively. This has opened the door to innovative research on LLM-powered MASs, including their applications in decision-making (Huang et al., 2024) and macroeconomic simulations (Li et al., 2023).

Building on these developments, *Agentomics* is an exploratory project that leverages the `langroid` framework to simulate macroeconomic systems using intelligent agents. By integrating economic principles with cutting-edge AI, *Agentomics* investigates how agent interactions—representing banks, regulators, and the broader economy—can provide insights into financial stability and the ripple effects of policy decisions.

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


## References

1. **de Zarzà, I., de Curtò, J., Roig, G., Manzoni, P., Calafate, C. T.** (2023). Emergent Cooperation and Strategy Adaptation in Multi-Agent Systems: An Extended Coevolutionary Theory with LLMs. *Electronics*, 12(2722). https://doi.org/10.3390/electronics12122722

2. **Guo, T., Chen, X., Wang, Y., Chang, R., Pei, S., Chawla, N. V., Wiest, O., Zhang, X.** Large Language Model-based Multi-Agents: A Survey of Progress and Challenges. *arXiv.org*. https://doi.org/10.48550/arXiv.2402.01680

3. **Huang, J., Li, E. J., Lam, M. H., Liang, T., Wang, W., Yuan, Y., Jiao, W., Wang, X., Tu, Z., Lyu, M. R.** How Far Are We on the Decision-Making of LLMs? Evaluating LLMs’ Gaming Ability in Multi-Agent Environments. *arXiv.org*. https://arxiv.org/abs/2403.11807

4. **Li, N., Gao, C., Li, Y., Liao, Q.** (2023). Large Language Model-Empowered Agents for Simulating Macroeconomic Activities. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.2310.10436
