# rules_bc.py

from __future__ import with_statement
import itertools
from pyke import contexts, pattern, bc_rule

pyke_version = '1.1.1'
compiler_version = 1

def welcome(rule, arg_patterns, arg_context):
  engine = rule.rule_base.engine
  patterns = rule.goal_arg_patterns()
  if len(arg_patterns) == len(patterns):
    context = contexts.bc_context(rule)
    try:
      if all(itertools.imap(lambda pat, arg:
                              pat.match_pattern(context, context,
                                                arg, arg_context),
                            patterns,
                            arg_patterns)):
        rule.rule_base.num_bc_rules_matched += 1
        with engine.prove('GenericContext', 'Signal', context,
                          (rule.pattern(0),
                           rule.pattern(1),)) \
          as gen_1:
          for x_1 in gen_1:
            assert x_1 is None, \
              "rules.welcome: got unexpected plan from when clause 1"
            rule.rule_base.num_bc_rule_successes += 1
            yield
        rule.rule_base.num_bc_rule_failures += 1
    finally:
      context.done()

def populate(engine):
  This_rule_base = engine.get_create('rules')
  
  bc_rule.bc_rule('welcome', This_rule_base, 'toret',
                  welcome, None,
                  (pattern.pattern_literal('welcome'),
                   contexts.variable('som'),
                   pattern.pattern_literal('hol'),),
                  (),
                  (pattern.pattern_literal('itsSignal'),
                   contexts.variable('som'),))


Krb_filename = 'rules.krb'
Krb_lineno_map = (
    ((16, 20), (2, 2)),
    ((22, 28), (4, 4)),
)
