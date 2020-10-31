A Python Implementation of a Statistical Model of Criminal Behavior
===================================================================

Description
-----------

This is a python implementation of the statistical model of criminal
behavior described by Short, D’Orsogno, Pasour, Tita, Brantingham,
Bertozzi and Chayes in their paper “A Statistical Model of Criminal
Behavior” published in Mathematical Models and Methods in Appliend
Sciences, Vol 18, Suppl (2008) 1249–1267.

The model is implemented in python using the Mesa library for agent
based modeling.

The model consists of a neighborhood of houses. Each house has an
attractiveness score:

.. math:: A = B_s + A_0

The attractiveness score is composed of a baseline attractiveness
:math:`A_0` and a dynamic component :math:`B_s`.

:math:`B_s` is determined by its previous value, the number of crimes
committed at an address in a previous period, and a broken windows
effect:

.. math:: B(t+\delta t) =  (B_s(t) + \frac{\mu l^2}{z} \Delta B_s(t))(1-\omega \delta t)+\theta E_s(t)

Where :math:`\delta` is the time interval, :math:`\mu` describes how
attractiveness spreads due to the broken window effect, :math:`l` is the
distance between houses, :math:`\Delta` is the discrete Laplacian
operator, :math:`z` is the number of houses around any single house (in
this case 4), :math:`\omega` describes attractiveness decay,
:math:`\theta` measures the attractiveness increase for crimes committed
at a location in the interval :math:`\delta t`.

Model Components
----------------

The model has three components. First, agents that represent houses.
Second, the criminal agents. Third, the spacial component represented by
a grid on a taurus.

Running main will run the model through the designated number of
iterations and output a heatmap of attractiveness.

At each step the datacollector summarizes, min, max and mean
attractiveness scores as well as the location of the house with the
maximum attractiveness.

