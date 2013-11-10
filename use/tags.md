---
title: Substitution tags
layout: default
---

*Templater* supports the following substitution tags in skeletons:

### Everywhere

**`{% raw %}{{code}}{% endraw %}`**: a unique alphanumeric code chosen when the *Templater* is run. Used to help ensure that participants only submit one survey per experiment.

**`{% raw %}{{total_number}}{% endraw %}`**: the number of items presented in the experiment.

### Within the items block

The items block begins with `{% raw %}{{#items}}` and ends with `{{/items}}{% endraw %}`. Its contents will be duplicated as many times as necessary by the *Templater*. The following substitution tags only apply within the items block:

**`{% raw %}{{number}}{% endraw %}`**: the current item number in the experiment.

**`{% raw %}{{field_n}}`**: will display the *n*-th field in the current item, on AMT or when simulated using the *Simulator*. Technically, `{{field_n}}{% endraw %}` for item number *m* is turned into `${field_m_n}` in the template file.