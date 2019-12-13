# MkDocs Branch Customization Plugin

This plugin allows configuration options to be overridden on a per-branch basis.
Branches are matched with regular expressions.

An example for adding CSS to the `master` branch might be:

```YAML
plugins:
  - branchcustomization:
      update_config:
        - branch: /master/
          extra_css:
            - css/master_branch.css
```

Note that this will *override* the global `extra_css` value.

To customize every branch *except* `master`:

```YAML
plugins:
  - branchcustomization:
      update_config:
        - branch: /(?!^master$)/
          +extra_css:
            - css/draft.css
          extra_js:
            - js/draft.js
```

In this case the `+extra_css` indicates that this list should be *appended* to
the global `extra_css` value, rather than overriding it, while `extra_js` overrides
the global value.
