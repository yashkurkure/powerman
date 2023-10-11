# Power Consumption of Heterogeneous Clusters of Chameleon

Chameleon is a large-scale, deeply reconfigurable experimental platform built to support Computer Sciences systems research. Chameleon is suitable for research in power consumption of heterogeneous computing systems as it supports a bare metal reconfiguration system giving users full control of the software stack including root privileges, kernel customization, and console access.

## Chameleon reserving resources
Chameleon resources are available at multiple sites, e.g., CHI@TACC, CHI@UC, CHI@Edge. Each of the sites host their own resources for each project to use. It is possible to lease resources at each chameleon site. The maximum length of a lease is 7 days. You can find more details about reservations [here](https://chameleoncloud.readthedocs.io/en/latest/technical/reservations.html).

Once a reservation is obtained for a device, a bare metal instance can be launched with various options of images such as Ubuntu, CentOS, etc. More on launching instances and setting up ssh access can be found [here](https://chameleoncloud.readthedocs.io/en/latest/technical/baremetal.html).




## References

### Links
* https://web.eece.maine.edu/~vweaver/projects/rapl/rapl_support.html
* https://ark.intel.com/content/www/us/en/ark/products/120483/intel-xeon-gold-6126-processor-19-25m-cache-2-60-ghz.html
* https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/running-average-power-limit-energy-reporting.html
* https://vstinner.github.io/intel-cpus.html#:~:text=The%20processor%20P%2Dstate%20is,some%20penalty%20to%20CPU%20performance.
* https://www.youtube.com/watch?v=1Rl8PyuK6yA
* https://www.reddit.com/r/Fedora/comments/11lh9nn/set_nvidia_gpu_power_and_temp_limit_on_boot/

### Papers
* https://dl.acm.org/doi/10.1145/2989081.2989088
* https://ieeexplore.ieee.org/document/9139675
* https://ieeexplore.ieee.org/document/6557170

