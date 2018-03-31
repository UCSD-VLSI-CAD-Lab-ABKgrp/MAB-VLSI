Introduction
=============

Designer access to leading-edge IC technology is challenged by the difficulty and cost of todays design process. Both human cost (i.e., engineering expertise and effort) and schedule cost (i.e., design schedule) are barriers to design at the leading edge. In advanced nodes, an added challenge to cost-effective design is that tools and flows are increasingly complex and noisy. Notably, very minute perturbations to constraints can result in very large variations in design flow outcomes. Yet, product companies must achieve the best possible design quality, within prescribed bounds of humans, licenses, CPUs, schedule and with acceptable probability of success. We cast the problem of optimally applying a budget of tool runs and schedule across different synthesis target frequencies as an instance of the classic multi-armed bandit problem, and implement a no-human-in-the-loop methodology that strategically samples target frequencies of individual tool runs.

Our tool solves two major problems that are of interest to designers; (i) Maximizing the performance of a chip and (ii) Maximizing the profit from chip design. Both problems are cast as different instances of the multi-armed bandit problem with varying reward functions.

Problem 1: Maximizing Performance
_________________________________

In Problem 1, we aim to maximize the performance of a design, subject to area and timing constraints, having no prior knowledge of achievable design metrics (area, power and maximum operating frequency). Typically, designers try to meet a specified target frequency of operation (spec) for a design. When this spec is not met, multiple iterations of Engineering Change Orders (ECOs) are performed until the target frequency is met. This process consumes considerable human effort and schedule. Here, we seek to characterize and exploit tool noise with a strategy that increases the probability of meeting a given frequency spec (as compared to naive denoising), within a budget of tool runs.

Problem 2: Maximizing Profit
____________________________

Problem 2 seeks to maximize the "profit" of a chip design, by optimizing a function of its area and frequency. Manufacturing cost of a chip increases with area. On the other hand, the selling price of a chip increases with operating frequency. For the purposes of our study here, we define a metric, "cost", as a measure of the combined effect of area and frequency on the profitability of a chip. Our aim is to minimize cost, thus maximizing profitability of the chip.

A document detailing our experiments proving the existence of noise in EDA tools and flows, along with our models to solve Problems 1 and 2 can be found `here <http://vlsicad.ucsd.edu/MAB/MAB_v7.pdf>`_. This work has been accepted as a Work-In-Progress Presentation at DAC 2018.