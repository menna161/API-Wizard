import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


def evaluate(self, room: 'Room', when: datetime.datetime) -> T.Optional[ScheduleEvaluationResultType]:
    'Evaluates the schedule, computing the value for the time the\n        given datetime object represents. The resulting value, a set of\n        markers applied to the value and the matching rule are returned.\n        If no value could be found in the schedule (e.g. all rules\n        evaluate to Next()), None is returned.'

    def log(msg: str, path: RulePath, *args: T.Any, **kwargs: T.Any) -> None:
        'Wrapper around room.log that prefixes spaces to the\n            message based on the length of the rule path.'
        prefix = (((' ' * 4) * max(0, (len(path.rules) - 1))) + '├─')
        room.log('{} {}'.format(prefix, msg), *args, **kwargs)
    room.log('Assuming it to be {}.'.format(when), level='DEBUG')
    expr_cache = {}
    expr_env = None
    markers = set()
    postprocessors = []
    paths = list(self.unfolded)
    path_idx = 0
    while (path_idx < len(paths)):
        path = paths[path_idx]
        path_idx += 1
        last_rule = path.rules[(- 1)]
        if isinstance(last_rule, SubScheduleRule):
            log('[SUB]  {}'.format(path), path, level='DEBUG')
            continue
        if (not path.is_active(when)):
            log('[INA]  {}'.format(path), path, level='DEBUG')
            continue
        log('[ACT]  {}'.format(path), path, level='DEBUG')
        result = None
        for rule in reversed(path.rules_with_expr_or_value):
            if (rule.expr is not None):
                plain_value = False
                try:
                    result = expr_cache[rule.expr]
                except KeyError:
                    if (expr_env is None):
                        expr_env = expression.build_expr_env(room, when)
                    result = room.eval_expr(rule.expr, expr_env)
                    expr_cache[rule.expr] = result
                    log('=> {}'.format(repr(result)), path, level='DEBUG')
                    if isinstance(result, expression.types.Mark):
                        result = result.unwrap(markers)
                else:
                    log('=> {}  [cache-hit]'.format(repr(result)), path, level='DEBUG')
                if isinstance(result, Exception):
                    room.log('Failed expression: {}'.format(repr(rule.expr_raw)), level='ERROR')
            elif (rule.value is not None):
                plain_value = True
                result = rule.value
                log('=> {}'.format(repr(result)), path, level='DEBUG')
            if (isinstance(result, expression.types.IncludeSchedule) and path.includes_schedule(result.schedule)):
                log('==   skipping in favour of parent to prevent cycle', path, level='DEBUG')
                result = None
            elif ((result is None) or isinstance(result, expression.types.Inherit)):
                log('==   skipping in favour of parent', path, level='DEBUG')
                result = None
            else:
                break
        if (result is None):
            room.log('No expression/value definition found, skipping {}.'.format(path), level='WARNING')
        elif isinstance(result, Exception):
            room.log('Evaluation failed, skipping {}.'.format(path), level='WARNING')
        elif isinstance(result, expression.types.Abort):
            break
        elif isinstance(result, expression.types.Break):
            prefix_size = max(0, (len(path.rules) - result.levels))
            prefix = path.rules[:prefix_size]
            log('== breaking out of {}'.format(prefix), path, level='DEBUG')
            while ((path_idx < len(paths)) and (paths[path_idx].root_schedule == path.root_schedule) and (paths[path_idx].rules[:prefix_size] == prefix)):
                del paths[path_idx]
        elif isinstance(result, expression.types.IncludeSchedule):
            _path = path.copy()
            _path.pop()
            _path.append(SubScheduleRule(result.schedule))
            paths.insert(path_idx, _path)
            for (i, sub_path) in enumerate(result.schedule.unfolded):
                paths.insert(((path_idx + i) + 1), (_path + sub_path))
        elif isinstance(result, expression.types.Postprocessor):
            if isinstance(result, expression.types.PostprocessorValueMixin):
                value = room.validate_value(result.value)
                if (value is None):
                    room.log('Aborting schedule evaluation.', level='ERROR')
                    break
                result.value = value
            postprocessors.append(result)
        elif isinstance(result, expression.types.Next):
            continue
        else:
            postprocessor_markers = set()
            result = room.validate_value(result)
            if ((result is None) and plain_value):
                room.log("Maybe this is an expression? If so, set it as the rule's 'expression' parameter rather than as 'value'.", level='WARNING')
            elif postprocessors:
                room.log('Applying postprocessors.', level='DEBUG')
                for postprocessor in postprocessors:
                    if (result is None):
                        break
                    markers.update(postprocessor_markers)
                    postprocessor_markers.clear()
                    room.log('+ {}'.format(repr(postprocessor)), level='DEBUG')
                    try:
                        result = postprocessor.apply(result)
                    except expression.types.PostprocessingError as err:
                        room.log('Error while applying {} to result {}: {}'.format(repr(postprocessor), repr(result), err), level='ERROR')
                        result = None
                        break
                    room.log('= {}'.format(repr(result)), level='DEBUG')
                    if isinstance(result, expression.types.Mark):
                        result = result.unwrap(postprocessor_markers)
                    result = room.validate_value(result)
            if (result is None):
                room.log('Aborting schedule evaluation.', level='ERROR')
                break
            markers.update(postprocessor_markers)
            room.log('Final result: {!r}, markers: {}'.format(result, markers), level='DEBUG')
            return (result, markers, last_rule)
    room.log('Found no result.', level='DEBUG')
    return None
