PyConntrack -- Another nf_conntrack convert
===========================================

Different from `pynetfilter_conntrack <https://github.com/regit/pynetfilter_conntrack>`, PyConntrack focus on converting conntrack data as json.


Installation
------------

To install Requests, simply:

.. code-block:: bash

    $ pip install pyconntrack


Usage
-----

- run as python module.
    .. code-block:: bash

        $ python -m pyconntrack -n 4 list

- use as python module.

    .. code-block:: python

        >>> from pyconntrack import NFConntrack
        >>> conntrack = NFConntrack()
        >>> conntrack.fetch_conntrack()
        >>> conntrack.forward("", "")
        >>> conntrack.server("", "")
        >>> conntrack.client("", "")
