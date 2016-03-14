itgetlink.backend
~~~~~~~~~~~~~~~~~~~~~

A set of micro services that handle incoming and outgoing messages (sms, email, etc).

Collaboration
=============

We're embracing simple workflow as following:

* ``master`` branch keeps production-ready deploy-able code.
* ``develop`` branch keeps in-progress code, e.g. features. Also, we use topic branch for feature.
* If ``master`` is buggy, checkout from it into a topic branch.
  Merge to ``master`` (and likely ``develop`` as well) after it has been done.
* If in doubt, always use topic branch and ask for design and/or implementation review from peers.
