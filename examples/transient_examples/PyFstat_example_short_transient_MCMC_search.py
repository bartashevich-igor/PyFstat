#!/usr/bin/env python

"""
Title
=====
An example MCMC-based search for a short transient signal.
"""

import pyfstat
import os
import numpy as np
import PyFstat_example_make_data_for_short_transient_search as data

if __name__ == "__main__":

    if not os.path.isdir(data.outdir) or not np.any(
        [f.endswith(".sft") for f in os.listdir(data.outdir)]
    ):
        raise RuntimeError(
            "Please first run PyFstat_example_make_data_for_short_transient_search.py !"
        )

    inj = {
        "tref": data.tstart,
        "F0": data.F0,
        "F1": data.F1,
        "F2": data.F2,
        "Alpha": data.Alpha,
        "Delta": data.Delta,
        "transient_tstart": data.transient_tstart,
        "transient_duration": data.transient_duration,
    }

    DeltaF0 = 1e-2
    DeltaF1 = 1e-9

    theta_prior = {
        "F0": {
            "type": "unif",
            "lower": inj["F0"] - DeltaF0 / 2.0,
            "upper": inj["F0"] + DeltaF0 / 2.0,
        },
        "F1": {
            "type": "unif",
            "lower": inj["F1"] - DeltaF1 / 2.0,
            "upper": inj["F1"] + DeltaF1 / 2.0,
        },
        "F2": inj["F2"],
        "Alpha": inj["Alpha"],
        "Delta": inj["Delta"],
        "transient_tstart": {
            "type": "unif",
            "lower": data.tstart,
            "upper": data.tstart + data.duration - 2 * data.Tsft,
        },
        "transient_duration": {
            "type": "unif",
            "lower": 2 * data.Tsft,
            "upper": data.duration - 2 * data.Tsft,
        },
    }

ntemps = 2
log10beta_min = -1
nwalkers = 100
nsteps = [200, 200]

    mcmc = pyfstat.MCMCTransientSearch(
        label="transient_search",
        outdir=data.outdir,
        sftfilepattern=os.path.join(data.outdir, "*simulated_transient_signal*sft"),
        theta_prior=theta_prior,
        tref=inj["tref"],
        nsteps=nsteps,
        nwalkers=nwalkers,
        ntemps=ntemps,
        log10beta_min=log10beta_min,
        transientWindowType="rect",
    )
    mcmc.run(walker_plot_args={"plot_det_stat": True, "injection_parameters": inj})
    mcmc.print_summary()
    mcmc.plot_corner(add_prior=True, truths=inj)
    mcmc.plot_prior_posterior(injection_parameters=inj)
