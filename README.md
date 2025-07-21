# traceroute
Example plugin for OpenPanel

This is an example plugin for OpenPanel.

[![2025-07-21-14-34.png](https://i.postimg.cc/X7cTZdzx/2025-07-21-14-34.png)](https://postimg.cc/w7MWZyHs)


---

To install it:

```
cd /etc/openpanel/modules
git clone https://github.com/stefanpejcic/traceroute
```

Then enable it from **OpenAdmin > Plans > Feature Manager** for desired feature plans.

After OpenPanel service restart, it will immediately be available to users on hositng plan that have that feature set assigned.


---

## Customization

There are a few rules to follow:

- readme.txt must be present for module to be visible
- .py file must have same name as the folder
