# `scikit-hep`: metapackage for Scikit-HEP

[![Scikit-HEP](https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg)](https://scikit-hep.org/)
[![Gitter](https://img.shields.io/gitter/room/gitterHQ/gitter.svg)](https://gitter.im/Scikit-HEP/community)
[![PyPI Package latest release](https://img.shields.io/pypi/v/scikit-hep.svg)](https://pypi.python.org/pypi/scikit-hep)
[![Conda latest release](https://img.shields.io/conda/vn/conda-forge/scikit-hep.svg)](https://github.com/conda-forge/scikit-hep-feedstock)
[![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1043949.svg)](https://doi.org/10.5281/zenodo.1043949)
[![GitHub Actions Status: CI](https://github.com/scikit-hep/scikit-hep/workflows/CI/badge.svg)](https://github.com/scikit-hep/scikit-hep/actions?query=workflow%3ACI+branch%3Amain)

## Project info

The [Scikit-HEP project](http://scikit-hep.org/) is a community-driven
and community-oriented project with the aim of providing Particle
Physics at large with an ecosystem for data analysis in Python embracing
all major topics involved in a physicist\'s work. The project started in
Autumn 2016 and its packages are actively developed and maintained.
Packages from Scikit-HEP are presently used by several major experiments.

It is not just about providing core and common tools for the community.
It is also about improving the interoperability between HEP tools and
the broad scientific ecosystem in Python, and about improving on
discoverability of utility packages and projects.

For what concerns the project grand structure, it should be seen as a
*toolset* rather than a toolkit.

**Getting in touch**

There are various ways to [get in
touch](https://scikit-hep.org/getting-in-touch.html) with project admins
and/or users and developers.

## scikit-hep package

`scikit-hep` is a metapackage for the Scikit-HEP project.

### Installation

You can install this metapackage from PyPI with \`pip\`:

```bash
python -m pip install scikit-hep
```

or you can use Conda through conda-forge:

```bash
conda install -c conda-forge scikit-hep
```

All the normal best-practices for Python apply; you should be in a
virtual environment, etc.

### Package version and dependencies

Please check the `setup.cfg` and `requirements.txt` files for the list
of Python versions supported and the list of Scikit-HEP project packages
and dependencies included, respectively.

For any installed `scikit-hep` the following displays the actual
versions of all Scikit-HEP dependent packages installed, for example:

```python
>>> import skhep
>>> skhep.show_versions()

System:
    python: 3.12.3 | packaged by conda-forge | (main, Apr 15 2024, 18:20:11) [MSC v.1938 64 bit (AMD64)]
executable: C:\Users\eduar\miniconda3\python.exe
   machine: Windows-11-10.0.26100-SP0

Python dependencies:
setuptools: 75.1.0
       pip: 24.2
     numpy: 2.0.1
     scipy: 1.15.1
    pandas: 2.2.3
matplotlib: 3.10.0

Scikit-HEP package version and dependencies:
        awkward: 2.8.1
boost_histogram: 1.5.0
  decaylanguage: 0.18.6
       hepstats: 0.9.2
       hepunits: 2.3.5
           hist: 2.8.0
     histoprint: 2.6.0
        iminuit: 2.30.1
         mplhep: 0.3.55
       particle: 0.25.2
          pylhe: 0.9.1
       resample: 1.10.1
     scikit-hep: 2025.4.1
         uproot: 5.6.0
         vector: 1.6.1
```

**Note on the versioning system:**

This package uses [Calendar Versioning](https://calver.org/) (CalVer).

## Contributors

We would like to acknowledge the contributors that made this project possible ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://cern.ch/eduardo.rodrigues"><img src="https://avatars.githubusercontent.com/u/5013581?v=4?s=100" width="100px;" alt="Eduardo Rodrigues"/><br /><sub><b>Eduardo Rodrigues</b></sub></a><br /><a href="#maintenance-eduardo-rodrigues" title="Maintenance">🚧</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=eduardo-rodrigues" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=eduardo-rodrigues" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://iscinumpy.dev"><img src="https://avatars.githubusercontent.com/u/4616906?v=4?s=100" width="100px;" alt="Henry Schreiner"/><br /><sub><b>Henry Schreiner</b></sub></a><br /><a href="#maintenance-henryiii" title="Maintenance">🚧</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=henryiii" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=henryiii" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/marinang"><img src="https://avatars.githubusercontent.com/u/24250309?v=4?s=100" width="100px;" alt="Matthieu Marinangeli"/><br /><sub><b>Matthieu Marinangeli</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=marinang" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=marinang" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jpivarski"><img src="https://avatars.githubusercontent.com/u/1852447?v=4?s=100" width="100px;" alt="Jim Pivarski"/><br /><sub><b>Jim Pivarski</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=jpivarski" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=jpivarski" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pollackscience"><img src="https://avatars.githubusercontent.com/u/5065341?v=4?s=100" width="100px;" alt="Brian Pollack"/><br /><sub><b>Brian Pollack</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=pollackscience" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=pollackscience" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/VanyaBelyaev"><img src="https://avatars.githubusercontent.com/u/17701591?v=4?s=100" width="100px;" alt="VanyaBelyaev"/><br /><sub><b>VanyaBelyaev</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=VanyaBelyaev" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=VanyaBelyaev" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://nils-braun.github.io/"><img src="https://avatars.githubusercontent.com/u/6116188?v=4?s=100" width="100px;" alt="Nils Braun"/><br /><sub><b>Nils Braun</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=nils-braun" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=nils-braun" title="Documentation">📖</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://www.matthewfeickert.com/"><img src="https://avatars.githubusercontent.com/u/5142394?v=4?s=100" width="100px;" alt="Matthew Feickert"/><br /><sub><b>Matthew Feickert</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=matthewfeickert" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=matthewfeickert" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://andrzejnovak.github.io/"><img src="https://avatars.githubusercontent.com/u/13226500?v=4?s=100" width="100px;" alt="Andrzej Novak"/><br /><sub><b>Andrzej Novak</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=andrzejnovak" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://alex.pearwin.com"><img src="https://avatars.githubusercontent.com/u/540853?v=4?s=100" width="100px;" alt="Alex Pearwin"/><br /><sub><b>Alex Pearwin</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=alexpearce" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ch.linkedin.com/in/mazurov"><img src="https://avatars.githubusercontent.com/u/75759?v=4?s=100" width="100px;" alt="Alexander Mazurov"/><br /><sub><b>Alexander Mazurov</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=mazurov" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/chrisburr"><img src="https://avatars.githubusercontent.com/u/5220533?v=4?s=100" width="100px;" alt="Chris Burr"/><br /><sub><b>Chris Burr</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=chrisburr" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/noeldawe/"><img src="https://avatars.githubusercontent.com/u/202816?v=4?s=100" width="100px;" alt="Noel Dawe"/><br /><sub><b>Noel Dawe</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=ndawe" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://orcid.org/0000-0002-2966-7461"><img src="https://avatars.githubusercontent.com/u/5884065?v=4?s=100" width="100px;" alt="Lukas Koch"/><br /><sub><b>Lukas Koch</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=ast0815" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=ast0815" title="Documentation">📖</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/HDembinski"><img src="https://avatars.githubusercontent.com/u/2631586?v=4?s=100" width="100px;" alt="Hans Dembinski"/><br /><sub><b>Hans Dembinski</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=HDembinski" title="Code">💻</a> <a href="https://github.com/scikit-hep/scikit-hep/commits?author=HDembinski" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jeremymcrae"><img src="https://avatars.githubusercontent.com/u/1767732?v=4?s=100" width="100px;" alt="Jeremy McRae"/><br /><sub><b>Jeremy McRae</b></sub></a><br /><a href="https://github.com/scikit-hep/scikit-hep/commits?author=jeremymcrae" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification.
