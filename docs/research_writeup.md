# Agentomics: Simulating Macroeconomic Dynamics with Intelligent Agents

Author: Akhil Karra \
*Undergraduate 3rd-Year Student at Carnegie Mellon University studying Mathematics, with a concentration in Statistics, and AI.*

```{contents}
:depth: 2
```

## Introduction

Understanding macroeconomic systems requires dissecting complex interactions among financial institutions, regulatory bodies, and market forces. These interactions, shaped by decisions of interdependent agents, present a challenge for researchers seeking to model and analyze emergent behaviors within such systems. Traditional approaches, such as rule-based models or game theory, often struggle to capture the dynamic and heterogeneous nature of these interactions (de Zarzà et al., 2023).

Recent advancements in Artificial Intelligence (AI), particularly Large Language Models (LLMs), have introduced new possibilities for modeling multi-agent systems (MASs). LLMs provide agents with advanced reasoning capabilities, enabling them to process nuanced inputs, adapt to changing environments, and communicate effectively. This has opened the door to innovative research on LLM-powered MASs, including their applications in decision-making (Huang et al., 2024) and macroeconomic simulations (Li et al., 2023).

Building on these developments, *Agentomics* is an exploratory project that leverages the Langroid framework to simulate macroeconomic systems using intelligent agents. By integrating economic principles with cutting-edge AI, this project investigates how agent interactions—representing banks, regulators, and the broader economy—can provide insights into financial stability and the ripple effects of policy decisions.

This project also reflects a personal journey of learning. Much of the work involved understanding MASs, becoming proficient with Langroid, and designing agent behaviors to align with macroeconomic concepts. The economic insights gained, though preliminary, highlight the potential of combining MASs and LLMs for studying complex systems.


## Simulation Overview

The *Agentomics* project focuses on modeling macroeconomic dynamics through a simulation involving four distinct agents. Each agent is designed to reflect a specific role within the financial ecosystem, leveraging LLMs to make decisions, adjust parameters, and understand adjustments made by other agents.

### Agents

1. `SmallBank`: Represents community-focused financial institutions. These agents simulate localized lending and borrowing, highlighting their influence on regional economies.
2. `BigBank`: A proxy for large commercial banks with national or international reach. These agents manage large-scale lending operations, adjust reserve requirements, and interact heavily with regulatory policies.
3. `CentralBank`: Models regulatory authorities responsible for monetary policy. It executes actions such as adjusting interest rates and implementing quantitative easing to maintain economic stability.
4. `EconomyAgent`: This agent aggregates inputs and feedback from all others, ensuring the simulation’s cohesiveness and alignment with real-world economic dynamics.

Each agent’s behavior is powered by LLMs configured using Langroid’s flexible architecture. These LLMs are not fine-tuned and their hyperparameters and kept exactly the same as provided. The purpose is to gauge how well the LLMs simulate these agents based purely on the training data and architecture of the LLM itself.

I also chose to fix the model used for each agent as a control variable. In the experiments shown in this project, `gpt-4o-mini` was fixed as the LLM of choice for all agents.

### Global State

The simulation operates on a round-based architecture where agents communicate and interact based on defined parameters, or "knobs." Here are the knobs for each of the agents above:

1. `SmallBank`: The small community-focused commercial bank in this simulation deals with lending to consumers and small-businesses. As a result, its major decisions deal with deciding the **loans interest rate** and the **consumer loan focus** (a percentage representing how much of the loans are being provided to individual consumers rather than small businesses).
1. `BigBank`: While many of the large commercial banks also have arms in asset management, wealth mangement, and investments, I choose to focus on their lending practices since this is the primary lever with which large banks can stimulate spending or savings. Thus, the large commercial bank actively changes its **loan-to-deposit** ratio to change how aggressively or conservatively the bank lends money with respect to deposits. It also adjusts the **deposit interest rate** to change how much money the bank attracts, influencing the bank's liquidity.
1. `CentralBank`: Modeling after the Federal Reserve in the United States, this central banking authority changes the **target interest rate** charged between banks to borrow money and the **percent change in securities holdings** on its balance sheet to increase or decrease money supply.
1. `EconomyAgent`: This agent takes the adjustments and behaviors of the other banks and predicts how the economy would respond. In this project, the specific economic variables that this agent manipulates are the **GDP growth rate**, **unemployment rate**, and **inflation rate**, since all three of these rates are used frequently to analyze the state and health of the economy.

Interactions are facilitated by Langroid’s messaging and tooling frameworks, which enables agents to share information, negotiate, and respond to changes in their environment. These knobs are stored in a global state which is updated on each round of the simulation.

I made an emphasis to make these knobs represent percentage quantities because I wanted to debias the prompts to the LLMs as much as possible. Specifically, I wanted to remove any mention to a specific currency, a specific country, or a specific period of time from the prompts to prevent the LLM from regurgitating behaviors of agents in these eras. I went as far as to remove absolute quantities from the knobs in case the LLM makes an association with money values of different magnitudes to different countries.

{numref}`simulation-diagram` below shows the process diagram for a round of the simulation.

```{figure} ./simulation-diagram.png
---
height: 300px
name: simulation-diagram
---
Process diagram for the Agentomics simulation, including information flow to agents and global state updates.
```

## Experiments and Takeaways

I devised two experiments to better understand and analyze the system's feasibility and accuracy. The first experiment was a backtesting evaluation experiment to understand how the system performed compared to real-world data. The second experiment ran the simulation twice on two initial states with a slight perturbation in one variable and then showed how the simulations evolved differently over time.

### Experiment 1: Backtesting Evaluation

The purpose of this experiment was to evaluate the MAS's ability to conduct long-term forecasting given limited history, relying on the training data of the LLM to generate the forecasts. The simulation was given eight quarters of economic and central bank data in the USA starting 2018Q1 to 2020Q1 in the initial state, with the goal of forecasting the following quarters until 2024Q1. On each round, the previous prediction by the simulation was taken as the last recorded data point, again relying on the training data of the LLM to continue the series and make predictions.

The data provided to the simulation for this experiment was:
* quarterly GDP growth rate,
* quarterly unemployment rate,
* quarterly Consumer Price Index (CPI) readings,
* quarterly effective Federal Funds Rate set by the Federal Reserve, and
* quarterly measurements of the securities held outright by the Federal Reserve.

These series were sourced from the Federal Reserve Economic Data (FRED) database. The percent changes in quarterly CPI readings were then derived to create a series representing the quarterly inflation rate, and the percent changes in the quarterly securities held outright were derived as well.

These series were then incorporated into the initial global state as the initial economic variable values and the initial central bank knobs. This means that in the initial round of the simulation, all agents had access to these data points in the series. The simulation was then run all the way until 2024Q1 in the manner described above.

{numref}`evaluate-mas` shows the graphs generated for the economic variables and `CentralBank` knobs as a result of this backtesting evaluation. The data points in the red shaded region represent the data points given to the simulation initially as context, and the data points that follow show the predicted or actual readings of the respective series.

```{figure} ./evaluate-mas.png
---
name: evaluate-mas
---
Generated plots of economic variables and bank knobs from Experiment 1: Backtesting Evaluation. This experiment evaluates the long-term forecasting ability of the MAS. Red-shaded points represent points given in context while points after the red shading show either the predicted data points by the simulation or the actual recorded data points.
```

### Takeaways from Experiment 1

The main takeaway seen from these graphs is that the multi-agent system seems to predict general long-term trends in GDP growth rate and unemployment rate. This was actually to be expected since the data points given as context occurred prior to the COVID pandemic taking its toll on the US economy in 2020Q2. However, the fact that it predicted a relatively stable GDP growth rate around 2% and an unemployment rate of around 4%, and the data points post-COVID support these trends, means that the MAS does a good job predicting trends for these series specifically. This observation is worth further investigation in different time periods and different context windows for data points.

Another interesting observation is that the MAS predicted a constant increase in the inflation rate, which did not end up happening. This linear increase in inflation rate is particularly interesting as it seems to suggest an internal belief of a constant increase in the inflation rate, which suggest further investigation in this track.

As for how the Federal Reserve responded, the simulation did not do so well. This prompts the question of whether injecting actual values of preceding quarters into the simulation prior to starting the next round would improve the simulation's predictions for the target interest rate and changes in securities holdings.

### Experiment 2: Perturbate Variables

The purpose of this experiment was to evaluate the MAS's ability to predict evolution in macroeconomic dynamics given a perturbation in one of the variables. In an attempt to debias the simulation as much as possible, the data I provided in the initial state was randomized but within reasonable bounds representing the past 5 quarters of recorded data. The particular scenario I investigated in this experiment for this project was given a 1.0% increase in the latest reading for the target interest rate by `CentralBank`, how would the global state evolve over the next 5 quarters.

Two simulation runs were conducted. One simulation run was conducted wihout the 1.0% increase in the target interest rate, and this simulation run was deemed the "control" simulation. The other simulation run was conducted with the increase in the target interest rate and was deemed the "experimental" simulation.

{numref}`percolate-deltas` shows the generated graphs for the economic variables and bank knobs from experiment 2. Red-shaded points represent points given in context while points after the red shading show the predicted data points from the control or experimental simulations.

```{figure} ./percolate-deltas.png
---
name: percolate-deltas
---
Generated plots of economic variables and bank knobs from Experiment 2: Perturbate. Given a 1.0% increase in the latest reading for the target interest rate, this experiment shows how the MAS updates the global state over the next 5 quarters. Red-shaded points represent points given in context while points after the red shading show the predicted data points from the control or experimental simulations. Note the circled datapoint in the Target Interest Rate graph indicating the 1.0% increase in the target interest rate.
```

The main takeaway from this experiment is that on the particular data provided, this increase in the target interest rate would cause less of a decrease in the GDP growth rate, less of an increase in the unemployment rate, and a much lower overall inflation rate. Inflation rate is predicted to stay below 2.0%, which is commonly the goal set by the Federal Reserve in the United States as a long term inflation rate. The simulation predicted that large commercial banks would attempt to attract more money into the bank for liquidity in the form of a higher deposit interest rate, which tracks with how banks set their deposit interest rate according to the target interest rate. Interestingly, the simulation predicted that the large commercial bank would lend more aggressively first and then become more conservative according to the loan to deposit ratio. The small commercial bank seems to want to attract more consumer customers with decreasing loan interest rates and generally more of a focus on lending to consumers.

## Lessons Learned

While creating and running the simulations, I gained some valuable insights into the challenges and best practices of designing LLM-powered MASs. Two key lessons emerged from integrating Langroid and running simulations:

### Ensuring Sensible Outputs
One major challenge was ensuring that agent outputs were not only valid but also meaningful for the simulation. For instance, the `CentralBank` agent’s percent change in securities holdings had to represent a *percent* change, not an absolute change. While Langroid supports strong type assertions for elementary types (e.g., `int` or `float`) in Tools, more granular checks were necessary for this use case.

To address this, I developed custom types like `Percent` and `NonnegPercent`, which validate percentage values during initialization. Additionally, I created a `TypedArray` class to dynamically type-check lists of elements as they were updated. These tools streamlined the type-checking process, ensuring accurate and consistent agent behavior during simulation runs.

### Managing LLM Bias and Analyzing Raw Outputs
Another key lesson was the importance of reducing bias in LLM-generated responses and analyzing the raw outputs. For example, I designed prompts to place the agents in a fictional country with no temporal context or direct references to real-world events. Despite these efforts, the LLM mentioned the COVID pandemic when backtesting the system, even though no such data was explicitly provided. This highlighted how specific input values could implicitly trigger unexpected associations and correlations in an LLM, which warrants deeper study into what such associations exist and how to mitigate them.

This insight underscored a critical design consideration for LLM-powered MASs: natural language outputs may not always conform to expectations and can reflect latent biases in the model. Langroid simplifies extracting structured data from LLM outputs, but additional post-processing may be necessary to ensure validity and relevance for specific use cases.


## Future Directions

The insights gained and lessons learned from this project lead to several opportunities for future research based on the work done in *Agentomics*.

1. **Adding Additional Agents and Stock Market Metrics**
   - Future iterations of the MAS introduced here could include additional agents for asset/wealth management firms and private equity firms to include big players on the stock market and alternative markets. It could also include additions to the global state measuring the S&P 500 or a similar stock market index.
   - From the efficient market hypothesis, the stock market incorporates a lot of information about other markets and proceedings. Incorporating the stock market into the simulation might increase the accuracy of the overall simulation.

1. **Refining LLM Utilization**
   - While the current simulation leverages LLMs effectively, exploring techniques like fine-tuning or reinforcement learning could improve decision-making accuracy.
   - Testing additional LLMs with larger context windows and domain-specific training might resolve some current limitations, particularly information leakage and potential hardcoding of data into the LLM's training data.

1. **Further Analysis of Simulation Accuracy**
    - Using the backtesting evaluation framework, the simulation could be tested on different time periods to better test accuracy and associations for each of the variables and knobs
    - Using the pertubate variables experiment framework, the simulation could be tested on real data and be cross-referenced to existing economic simulations done using reaction functions to evaluate whether the assumption and predictions made by the model track with economic theory.

## Applications

This project opens several avenues for applying and extending multi-agent simulations in macroeconomics. While the project focused on exploring the feasibility of LLM-powered MASs to economic simulations and deriving some initial insights from such a system, the potential applications for these systems are broad and impactful.

1. **Economic Modeling**
   - By simulating interactions between banks, regulators, and the broader economy, LLM-powered MASs offers a framework for exploring systemic risks, financial stability, and the cascading effects of economic policies.
   - Researchers can use similar simulations to test hypotheses about macroeconomic behaviors, such as the impact of interest rate changes or lending policy adjustments.

2. **Educational Tools**
   - The project provides a hands-on, interactive environment for students and educators to explore complex economic concepts.
   - It can be adapted into classroom activities, where students experiment with different scenarios and observe the resulting macroeconomic dynamics.

3. **Policy Prototyping**
   - Policymakers can leverage MAS-based simulations to test the effects of proposed regulations in a risk-free virtual environment.
   - For example, adjustments to reserve requirements or interest rates can be studied to predict their outcomes on financial stability and market activity.

## Conclusion

The *Agentomics* project represents an exploration of modeling macroeconomic systems using LLM-powered Multi-Agent Systems (MASs). By leveraging the flexibility of the Langroid framework, the goal was not only to test the feasibility of such a system but also to derive preliminary insights into macroeconomic behaviors.

The experiments conducted revealed valuable takeaways:
- **Experiment 1 (Backtesting Evaluation)** showed the system’s strength in predicting long-term trends for GDP growth and unemployment rates, despite limitations in capturing certain variables like inflation or central bank responses. These insights underscore the potential of LLM-powered MASs in trend forecasting while identifying areas for refinement.
- **Experiment 2 (Perturbate Variables)** demonstrated the system’s capability to simulate the ripple effects of policy changes, such as a 1.0% increase in the target interest rate, on macroeconomic variables. The experiment highlighted nuanced agent behaviors, such as adjustments in lending practices and interest rates.

Key lessons emerged from this project, including the importance of ensuring sensible outputs, managing LLM biases, and analyzing raw outputs to better understand latent associations in LLMs. The project also revealed the technical challenges and opportunities of designing robust and meaningful simulations, such as using custom types to validate agent outputs and creating scenarios free from explicit real-world context to minimize bias.

Looking ahead, several future directions and applications extend the potential of *Agentomics*:
- Refining the MAS with additional agents and metrics, such as stock market indicators, can enhance its comprehensiveness and accuracy.
- Exploring advanced LLM utilization techniques like fine-tuning and reinforcement learning can improve decision-making capabilities.
- Further testing the system using backtesting and perturbation frameworks across different time periods and datasets can provide deeper insights and validate its consistency with economic theories.

Beyond research, this project opens avenues in education, policy prototyping, and economic modeling, offering an interactive tool for understanding complex systems and predicting policy outcomes.


## References

1. **de Zarzà, I., de Curtò, J., Roig, G., Manzoni, P., Calafate, C. T.** (2023). Emergent Cooperation and Strategy Adaptation in Multi-Agent Systems: An Extended Coevolutionary Theory with LLMs. *Electronics*, 12(2722). https://doi.org/10.3390/electronics12122722

2. **Guo, T., Chen, X., Wang, Y., Chang, R., Pei, S., Chawla, N. V., Wiest, O., Zhang, X.** Large Language Model-based Multi-Agents: A Survey of Progress and Challenges. *arXiv.org*. https://doi.org/10.48550/arXiv.2402.01680

3. **Huang, J., Li, E. J., Lam, M. H., Liang, T., Wang, W., Yuan, Y., Jiao, W., Wang, X., Tu, Z., Lyu, M. R.** How Far Are We on the Decision-Making of LLMs? Evaluating LLMs’ Gaming Ability in Multi-Agent Environments. *arXiv.org*. https://arxiv.org/abs/2403.11807

4. **Li, N., Gao, C., Li, Y., Liao, Q.** (2023). Large Language Model-Empowered Agents for Simulating Macroeconomic Activities. *arXiv (Cornell University)*. https://doi.org/10.48550/arxiv.2310.10436
