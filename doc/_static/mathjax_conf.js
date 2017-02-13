/*
 * This file configures MathJax, a JavaScript LaTeX renderer.
 * Full configuration information can be found here:
 *
 *     http://docs.mathjax.org/en/latest/configuration.html
 *
 * Principally, this file defines macros that MathJax will expand. The
 * TeX.Macros object maps macro names to LaTeX code.
 */
MathJax.Hub.Config({
    TeX: {
        Macros: {
            rapidity: 'y',
            pT: 'p_{\\mathrm{T}}',
            decay: ['#1 \\to #2', 2]
        }
    }
});
