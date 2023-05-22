import ast


#this function creates an ast tree based on this documentation: https://docs.python.org/3/library/ast.html
#based on the node and its edges a tree is created
def parse_ast(nodes, edges):
    # Create a dictionary of nodes
    ex =''
    root = ast.parse(ex)
    node_type= ''
    node_id = -1
    ast_nodes = {}
    #loop on all nodes and create a node based on their name
    for node in nodes:
        # Parse the node ID and type
        node_id = node_id+1
        node_type = node

        if node_type.startswith('Name#id'):
            # Parse the name and context of Name nodes
            name = node_type[8:]
            ast_node = ast.Name(id=name, ctx=ast.Load())
        elif node_type == 'Name':
          ast_node = ast.Name(id='PLACEHOLDER', ctx=ast.Load())
        elif node_type == 'Call':
            ast_node = ast.Call(func=ast.Name('PLACEHOLDER',None), args=[], keywords=[])
        elif node_type == 'Assign':
            ast_node = ast.Assign(targets=[], value=ast.Name(id='PLACEHOLDER', ctx=ast.Load()))
        elif node_type == 'Load':
            ast_node = ast.Load()
        elif node_type == 'Store':
            ast_node = ast.Store()
        elif node_type == 'Del':
            ast_node = ast.Del()

        elif node_type == 'Import':
            ast_node = ast.Import(names=[])
        elif node_type.startswith('ImportFrom'):
            module_name = node_type[18:]
            ast_node = ast.ImportFrom(module=module_name, names=[], level=0)

        elif node_type == 'Add':
            ast_node = ast.Add()
        elif node_type == 'Sub':
            ast_node = ast.Sub()
        elif node_type == 'Mult':
            ast_node = ast.Mult()
        elif node_type == 'MatMult':
            ast_node = ast.MatMult()
        elif node_type == 'Div':
            ast_node = ast.Div()
        elif node_type == 'Mod':
            ast_node = ast.Mod()
        elif node_type == 'Pow':
            ast_node = ast.Pow()
        elif node_type == 'LShift':
            ast_node = ast.LShift()
        elif node_type == 'RShift':
            ast_node = ast.RShift()
        elif node_type == 'BitOr':
            ast_node = ast.BitOr()
        elif node_type == 'BitXor':
            ast_node = ast.BitXor()
        elif node_type == 'BitAnd':
            ast_node = ast.BitAnd()
        elif node_type == 'FloorDiv':
            ast_node = ast.FloorDiv()
        elif node_type == 'Eq':
            ast_node = ast.Eq()
        elif node_type == 'NotEq':
            ast_node = ast.NotEq()
        elif node_type == 'Lt':
            ast_node = ast.Lt()
        elif node_type == 'LtE':
            ast_node = ast.LtE()
        elif node_type == 'Gt':
            ast_node = ast.Gt()
        elif node_type == 'GtE':
            ast_node = ast.GtE()
        elif node_type == 'Is':
            ast_node = ast.Is()
        elif node_type == 'IsNot':
            ast_node = ast.IsNot()
        elif node_type == 'In':
            ast_node = ast.In()
        elif node_type == 'NotIn':
            ast_node = ast.NotIn()

        elif node_type == 'BinOp':
          ast_node = ast.BinOp(left=None, op=None, right=None)
        
        elif node_type.startswith('alias'):
            
            first_eq_idx = node_type.find("=")
            next_char_idx = node_type.find("#", first_eq_idx)
            if next_char_idx == -1:
                next_char_idx = len(node_type)
            elif "\n" in node_type[first_eq_idx:next_char_idx]:
              next_char_idx = node_type.find("\n", first_eq_idx)

            second_eq_idx = node_type.find("=", first_eq_idx + 1)
            name = node_type[first_eq_idx + 1:next_char_idx].strip()
            if second_eq_idx==-1:
              ast_node = ast.alias(name,None)
            else:
              asname = node_type[second_eq_idx + 1:].strip()
              ast_node = ast.alias(name,asname)
            
        elif node_type == 'BoolOp':
            ast_node = ast.BoolOp(op=ast.And(), values=[])
        elif node_type == 'UnaryOp':
            ast_node = ast.UnaryOp(op=ast.UAdd(), operand=None)
        elif node_type == 'And':
            ast_node = ast.And()
        elif node_type == 'Not':
            ast_node = ast.Not()
        elif node_type == 'UAdd':
            ast_node = ast.UAdd()
        elif node_type == 'USub':
            ast_node = ast.USub()
        elif node_type == 'Invert':
            ast_node = ast.Invert()           
        elif node_type == 'Or':
          ast_node = ast.Or()
        elif node_type == 'NamedExpr':
          ast_node = ast.NamedExpr(target=None, value=None)
        elif node_type == 'Lambda':
          ast_node = ast.Lambda(args= ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=None)
        elif node_type == 'IfExp':
          ast_node = ast.IfExp(test=None, body=None , orelse= None)       
        elif node_type == 'Dict':
          ast_node = ast.Dict(keys=[], values=[])
        elif node_type == 'Set':
           ast_node = ast.Set(elts=[])
        elif node_type == 'ListComp':
          ast_node = ast.ListComp(elt=None, generators=[])
        elif node_type == 'SetComp':
          ast_node = ast.SetComp(elt=None, generators=[])
        elif node_type == 'DictComp':
          ast_node = ast.DictComp(key=None, value=None, generators=[])
        elif node_type == 'GeneratorExp':
           ast_node = ast.GeneratorExp(elt=None, generators=[])
        elif node_type == 'comprehension':
          ast_node = ast.comprehension(target=None, iter=None, ifs=[], is_async=False)
        elif node_type == 'Compare':
          ast_node = ast.Compare(left=None, ops=[], comparators=[])
          #NOT USED ANYMORE IN NEWER VERSIONS
        # elif node_type == 'MatchValue':
        #     ast_node = ast.MatchValue(value=None)
        # elif node_type == 'MatchSingleton':
        #     ast_node = ast.MatchSingleton(value=None)
        # elif node_type == 'MatchSequence':
        #     ast_node = ast.MatchSequence(patterns=[])
        # elif node_type == 'MatchMapping':
        #     ast_node = ast.MatchMapping(keys=[], patterns=[], rest=None)
        # elif node_type == 'MatchClass':
        #     ast_node = ast.MatchClass(cls=None, patterns=[], kwd_attrs=[], kwd_patterns=[])
        # elif node_type == 'MatchStar':
        #     ast_node = ast.MatchStar(name=None)
        # elif node_type == 'MatchAs':
        #     ast_node = ast.MatchAs(pattern=None, name=None)
        # elif node_type == 'MatchOr':
        #     ast_node = ast.MatchOr(patterns=[])

        elif node_type.startswith('FunctionDef'):
          func_name = node_type.split('=')[1]
          ast_node = ast.FunctionDef(name=func_name, args= ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[], decorator_list=[])
        elif node_type.startswith('AsyncFunctionDef'):
          func_name = node_type.split('=')[1]
          ast_node = ast.FunctionDef(name=func_name, args= ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[], decorator_list=[])
        elif node_type == 'Expr':
          ast_node = ast.Expr(ast.Name(id='PLACEHOLDER', ctx=ast.Load()))
        elif node_type.startswith('Constant'):
          tmp = node_type.split('=')[1]
          value_node = tmp.split('#')[0]
          kind_node = None
          if len(node_type.split('=')) > 2:
              tmp = node_type.split('=')[2]
              kind_node= tmp.split('#')[0]
          if(value_node.isdigit()):
            value_node= int(value_node)
          ast_node = ast.Constant(value=tmp,kind=kind_node)

        elif node_type == 'List':
          ast_node = ast.List(elts=[],ctx=ast.Load())
        elif node_type == 'Module':
          ast_node = ast.Module(body=[],type_ignores=[])
        elif node_type == 'arguments':
          ast_node = ast.arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])
        elif node_type.startswith('arg'):
          ast_node = ast.arg(arg='PLACEHOLDER', annotation=None, type_comment=None)
        elif node_type.startswith('ClassDef'):
          class_name = node_type.split('=')[1]
          ast_node = ast.ClassDef(name=class_name, bases=[], keywords=[], body=[], decorator_list=[])
        elif node_type.startswith('Attribute'):
          next_char_idx = node_type.find("#")
          if next_char_idx == -1:
            attr_name = 'PLACEHOLDER'
          else:
            attr_name = node_type.split('=')[1]
          ast_node = ast.Attribute(value=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), attr=attr_name, ctx=ast.Load())
        elif node_type.startswith('JoinedStr'):
          ast_node = ast.JoinedStr(values = [])
        elif node_type.startswith('FormattedValue'):
          conv_value = node_type.split('=')[1]
          ast_node = ast.JoinedStr(values = [], conversion = conv_value, format_spec=None)
        elif node_type.startswith('Return'):
          ast_node = ast.Return(value = None)
        elif node_type == 'Delete':
          ast_node = ast.Delete(targets = [])
        elif node_type == 'Del':
          ast_node = ast.Del()
        elif node_type == 'AugAssign':
          ast_node = ast.AugAssign(target = ast.Name(id='PLACEHOLDER', ctx=ast.Load()), op = None, value=None)
        elif node_type.startswith('AnnAssign'):
          simple_val = node_type.split('=')[1]
          ast_node = ast.AnnAssign(target = ast.Name(id='PLACEHOLDER', ctx=ast.Load()), annotation = ast.Name(id='Type', ctx=ast.Load()), value=None, simple=simple_val)
        elif node_type == 'For':
          ast_node = ast.For(target=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), iter=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), body=[], orelse=[], type_comment=None)
        elif node_type == 'AsyncFor':
          ast_node = ast.AsyncFor(target=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), iter=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), body=[], orelse=[], type_comment=None)
        elif node_type == 'While':
          ast_node = ast.While(test=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), body=[], orelse=[])
        elif node_type == 'If':
          ast_node = ast.If(test=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), body=[], orelse=[])
        elif node_type == 'With':
          ast_node = ast.With(items=[], body=[], type_comment=None)
        elif node_type == 'AsyncWith':
          ast_node = ast.AsyncWith(items=[], body=[], type_comment=None)
        elif node_type == 'withitem':
          ast_node = ast.withitem(context_expr=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), optional_vars=None)
        elif node_type == 'Raise':
            ast_node = ast.Raise(exc=None, cause=None)
        elif node_type == 'Try':
            ast_node = ast.Try(body=[], handlers=[], orelse=[], finalbody=[])
        elif node_type.startswith('ExceptHandler'):
            next_char_idx = node_type.find("#")
            if(next_char_idx == -1):
              ast_node = ast.ExceptHandler(type=None,name=None,body=[])
            else:
              except_name = node_type.split('=')[1]
              ast_node = ast.ExceptHandler(type=None,name=except_name,body=[])            
        elif node_type == 'Assert':
            ast_node = ast.Assert(test=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), msg=None)
        elif node_type.startswith('Global'):
            placeholders_count = int(node_type.split('=')[1])
            ast_node = ast.Global(names=[])
            while placeholders_count > 0:
              ast_node.names.append('PLACEHOLDER')
              placeholders_count -= 1 
        elif node_type.startswith('Nonlocal'):
            placeholders_count = int(node_type.split('=')[1])
            ast_node = ast.Nonlocal(names=[])
            while placeholders_count > 0:
              ast_node.names.append('PLACEHOLDER')
              placeholders_count -= 1
        elif(node_type == "Pass"):
          ast_node = ast.Pass()
        elif(node_type == "Break"):
          ast_node = ast.Break()
        elif(node_type == "Continue"):
          ast_node = ast.Continue()
        elif node_type == 'Await':
            ast_node = ast.Await(value=ast.Name(id='PLACEHOLDER', ctx=ast.Load()))
        elif node_type == 'Yield':
            ast_node = ast.Yield(value=None)
        elif node_type == 'YieldFrom':
            ast_node = ast.YieldFrom(value=ast.Name(id='PLACEHOLDER', ctx=ast.Load()))
        elif node_type == 'Subscript':
            ast_node = ast.Subscript(value=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), slice=None, ctx=ast.Load())
        elif node_type == 'Tuple':
          ast_node = ast.Tuple(elts=[], ctx=ast.Load())
        elif node_type == 'Slice':
          ast_node = ast.Slice(lower=None, upper=None, step=None)
        elif node_type == 'Starred':
          ast_node = ast.Starred(value=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), ctx=ast.Load())
        elif node_type.startswith('keyword'):
          next_char_idx = node_type.find("#")
          if(next_char_idx == -1):
            ast_node = ast.keyword(value=ast.Name(id='PLACEHOLDER', ctx=ast.Load()))
          else:
            arg_name = node_type.split('=')[1]
            ast_node = ast.keyword(arg=arg_name, value=ast.Name(id='PLACEHOLDER', ctx=ast.Load()))

        else:
            raise ValueError(f"Invalid node type: {node_type}")
        ast_nodes[node_id] = ast_node

    # Create the AST by adding edges                                                 
############################################################################ EDGES #########################################################################3
    #loop on all the edges and based on the edge label complete the arguments of the ast node
    for parent_id, child_id , edge_type in edges:
        parent_node = ast_nodes[parent_id]
        child_node = ast_nodes[child_id]

        if isinstance(parent_node, ast.Call):
            if edge_type.startswith('arg'):
                # Add the child node as an argument to the Call node
                parent_node.args.append(child_node)
            elif edge_type == 'func':
                # Set the child node as the function of the Call node
                parent_node.func = child_node
            elif edge_type.startswith('keywords'):
                # Add the child node as a keyword argument to the Call node
                key, value = child_node.arg, child_node.value
                parent_node.keywords.append(ast.keyword(arg=key, value=value))

        elif isinstance(parent_node, ast.Assign):
            # Add the child node as a target or value of the Assign node
            if edge_type.startswith('targets'):
                parent_node.targets.append(child_node)
            elif edge_type.startswith('value'):
                parent_node.value = child_node
            else:
                raise ValueError(f"Invalid edge: {parent_id} -> {child_id} {edge_type} {edge_type}")

        elif isinstance(parent_node, ast.Name):
          if edge_type == 'ctx':
            parent_node.ctx = child_node
        elif isinstance(parent_node, ast.Attribute):
            if edge_type == 'value':
                # Add the child node as an argument to the Call node
              parent_node.value = child_node
            elif edge_type == 'ctx':
              parent_node.ctx = child_node

        elif isinstance(parent_node, ast.Import):
            # Add the child node as a name of the Import node
            parent_node.names.append(child_node)

        elif isinstance(parent_node, ast.ImportFrom):
            # Set the child node as the module or name of the ImportFrom node
            if  edge_type == 'module':
                parent_node.module = child_node
            elif  edge_type.startswith('names'):
                parent_node.names.append(child_node)
            elif edge_type == 'level':
              parent_node.level = child_node
            else:
                raise ValueError(f"Invalid edge: {parent_id} -> {child_id} {edge_type}")
        elif isinstance(parent_node,  ast.BinOp):
          # Set the child node as the left or right operand of the Add or BinOp node
          if edge_type == 'op':
              parent_node.op = child_node
          elif edge_type == 'right':
              parent_node.right = child_node
          elif edge_type == 'left':
              parent_node.left = child_node
          else:
              raise ValueError(f"Invalid edge: {parent_id} -> {child_id} {edge_type}")

        elif isinstance(parent_node, (ast.Add, ast.Sub, ast.Mult, ast.MatMult, ast.Div, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd, ast.FloorDiv)):
           pass
        elif isinstance(parent_node, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn)):
          pass
        elif isinstance(parent_node,  ast.alias):
           pass
        elif isinstance(parent_node,  ast.Or):
           pass
        elif isinstance(parent_node,  ast.BoolOp):
          if edge_type == 'op':
            parent_node.op= child_node
          elif edge_type.startswith('values'):
            parent_node.values.append(child_node)
        elif isinstance(parent_node,  ast.NamedExpr):
          if edge_type == 'target':
            parent_node.target= child_node
          
          elif edge_type == 'value':
            parent_node.value = child_node
        elif isinstance(parent_node,  ast.UnaryOp):
          if edge_type == 'op':
            parent_node.op= child_node
          
          elif edge_type == 'operand':
            parent_node.operand = child_node
        elif isinstance(parent_node,  ast.Lambda):
          if edge_type .startswith('args'):   
                parent_node.args = child_node
          elif edge_type == 'body':
            parent_node.body = child_node
        elif isinstance(parent_node,  ast.IfExp):
          if edge_type == 'test':   
                parent_node.test = child_node
          elif edge_type == 'body':
            parent_node.body = child_node       
          elif edge_type == 'orelse':
            parent_node.orelse = child_node
        elif isinstance(parent_node, ast.Dict):
          if edge_type.startswith('keys'):
              parent_node.keys.append(child_node)
          elif edge_type.startswith('values'):
              parent_node.values.append(child_node)
        elif isinstance(parent_node, ast.Set):
          if edge_type.startswith('elts'):
            parent_node.elts.append(child_node)
        elif isinstance(parent_node, ast.ListComp):
          if edge_type == 'elt':
              parent_node.elt = child_node
          elif edge_type == 'generators':
              parent_node.generators.append(child_node)
        elif isinstance(parent_node, ast.SetComp):
          if edge_type == 'elt':
              parent_node.elt = child_node
          elif edge_type == 'generators':
              parent_node.generators.append(child_node)
        elif isinstance(parent_node, ast.DictComp):
          if edge_type == 'key':
              parent_node.key = child_node
          elif edge_type == 'value':
              parent_node.value = child_node
          elif edge_type == 'generators':
              parent_node.generators.append(child_node)
        elif isinstance(parent_node, ast.GeneratorExp):
          if edge_type == 'elt':
              parent_node.elt = child_node
          elif edge_type == 'generators':
              parent_node.generators.append(child_node)
        elif isinstance(parent_node, ast.comprehension):
          if edge_type == 'target':
              parent_node.target = child_node
          elif edge_type == 'iter':
              parent_node.iter = child_node
          elif edge_type.startswith('ifs'):
              parent_node.ifs.append(child_node)
          elif edge_type == 'is_async':
              parent_node.is_async = child_node
        elif isinstance(parent_node, ast.Compare):
          if edge_type == 'left':
              parent_node.left = child_node
          elif edge_type == 'ops':
              parent_node.ops.append(child_node)
          elif edge_type == 'comparators':
              parent_node.comparators.append(child_node)
              
              ########################## xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX NOT USED-MATCH XXXXXXXXXXXXXXXXXXXXX#########################3
        # elif isinstance(parent_node, (ast.MatchValue, ast.MatchSingleton, ast.MatchStar, ast.MatchAs)):
        #     if edge_type == 'value':
        #         parent_node.value = child_node
        #     elif edge_type == 'pattern':
        #         parent_node.pattern = child_node
        #     elif edge_type == 'name':
        #         parent_node.name = child_node
        # elif isinstance(parent_node, ast.MatchSequence):
        #   if edge_type == 'patterns':
        #       parent_node.patterns = child_node
        # elif isinstance(parent_node, ast.MatchMapping):
        #   if edge_type == 'keys':
        #       parent_node.keys = child_node
        #   elif edge_type == 'patterns':
        #       parent_node.patterns = child_node
        #   elif edge_type == 'rest':
        #       parent_node.rest = child_node
        # elif isinstance(parent_node, ast.MatchClass):
        #   if edge_type == 'cls':
        #       parent_node.cls = child_node
        #   elif edge_type == 'patterns':
        #       parent_node.patterns = child_node
        #   elif edge_type == 'kwd_attrs':
        #       parent_node.kwd_attrs = child_node
        #   elif edge_type == 'kwd_patterns':
        #       parent_node.kwd_patterns = child_node

        elif isinstance(parent_node,  ast.FunctionDef) or isinstance(parent_node,  ast.AsyncFunctionDef):
          if edge_type.startswith('args'):
            parent_node.args = child_node
          elif edge_type.startswith('body'):
            parent_node.body.append(child_node)
          elif edge_type == 'decorator_list':
            parent_node.decorator_list.append(child_node)
          elif edge_type == 'returns':
            parent_node.returns = child_node
        elif isinstance(parent_node,  ast.Expr):
          parent_node.value = child_node
        elif isinstance(parent_node,  ast.Constant):
          pass
        elif isinstance(parent_node,  ast.List):
          if edge_type.startswith('elts'):
              parent_node.elts.append(child_node)
          elif edge_type == 'ctx':
               parent_node.ctx = child_node
        elif isinstance(parent_node, ast.Module):
          if edge_type.startswith('body'):
            parent_node.body.append(child_node)
          elif edge_type == 'type_ignores':
            parent_node.type_ignores.append(child_node)
          root = parent_node
        elif isinstance(parent_node, ast.arguments):
          if edge_type == 'posonlyargs':
            parent_node.posonlyargs.append(child_node)
          elif edge_type.startswith('args'):
            parent_node.args.append(child_node)
          elif edge_type == 'vararg':
            parent_node.vararg = child_node
          elif edge_type == 'kwonlyargs':
            parent_node.kwonlyargs.append(child_node)
          elif edge_type == 'kw_defaults':
            parent_node.kw_defaults.append(child_node)
          elif edge_type == 'kwarg':
            parent_node.kwarg = child_node
          elif edge_type == 'defaults':
            parent_node.defaults.append(child_node)
        elif isinstance(parent_node, ast.arg):
          if edge_type == 'annotation':
            parent_node.annotation = child_node
          elif edge_type == 'type_comment':
            parent_node.type_comment = child_node
        elif isinstance(parent_node, ast.ClassDef):
          if edge_type == 'bases':
            parent_node.bases.append(child_node)
          elif edge_type.startswith('keywords'):
            parent_node.keywords.append(child_node)
          elif edge_type.startswith('body'):
            parent_node.body.append(child_node)
          elif edge_type == 'decorator_list':
            parent_node.decorator_list.append(child_node)
        elif isinstance(parent_node, ast.Attribute):
          if edge_type == 'name':
            parent_node.name = child_node
          elif edge_type == 'ctx':
            parent_node.ctx = child_node
        elif isinstance(parent_node, ast.JoinedStr):
          if edge_type == 'values':
            parent_node.values.append(child_node)
        elif isinstance(parent_node, ast.FormattedValue):
          if edge_type == 'values':
            parent_node.values.append(child_node)
          elif edge_type == 'format_spec':
            parent_node.format_spec = child_node
        elif isinstance(parent_node, ast.Return):
          if edge_type == 'value':
             parent_node.value = child_node
        elif isinstance(parent_node, ast.Delete):
          if edge_type.startswith('targets'):
             parent_node.targets.append(child_node)
        elif isinstance(parent_node,  ast.Del):
          pass
        elif isinstance(parent_node, ast.AugAssign):
          if edge_type == 'target':
            parent_node.target = child_node
          elif edge_type == 'op':
            parent_node.op = child_node
          elif edge_type == 'value':
            parent_node.value = child_node
        elif isinstance(parent_node, ast.AnnAssign):
          if edge_type == 'target':
            parent_node.target = child_node
          elif edge_type == 'annotation':
            parent_node.op = child_node
          elif edge_type == 'value':
            parent_node.value = child_node
        elif isinstance(parent_node, ast.For) or isinstance(parent_node, ast.AsyncFor):
          if edge_type == 'target':
            parent_node.target = child_node
          elif edge_type == 'iter':
            parent_node.iter = child_node
          elif edge_type.startswith('body'):
            parent_node.body.append(child_node)
          elif edge_type.startswith('orelse'):
            parent_node.orelse.append(child_node)
        elif isinstance(parent_node, ast.While) or isinstance(parent_node, ast.If):
          if edge_type == 'test':
            parent_node.test = child_node
          elif edge_type.startswith('body'):
            parent_node.body.append(child_node)
          elif edge_type.startswith('orelse'):
            parent_node.orelse.append(child_node)
        elif isinstance(parent_node, ast.With) or isinstance(parent_node, ast.AsyncWith):
          if edge_type.startswith('items'):
            parent_node.items.append(child_node)
          elif edge_type.startswith('body'):
            parent_node.body.append(child_node)
        elif isinstance(parent_node, ast.withitem):
          if edge_type == 'context_expr':
            parent_node.context_expr = child_node
          elif edge_type == 'optional_vars':
            parent_node.optional_vars = child_node
        elif isinstance(parent_node, ast.Raise):
          if edge_type == 'exc':
              parent_node.exc = child_node
          elif edge_type == 'cause':
              parent_node.cause = child_node
        elif isinstance(parent_node, ast.ExceptHandler):
          if edge_type == 'type':
              parent_node.type = child_node
          elif edge_type.startswith('body'):
              parent_node.body.append(child_node)
        elif isinstance(parent_node, ast.Try):
          if edge_type.startswith('body'):
            parent_node.body.append(child_node)
          elif edge_type.startswith('handlers'):
            parent_node.handlers.append(child_node)
          elif edge_type.startswith('orelse'):
            parent_node.orelse.append(child_node)
          elif edge_type.startswith('finalbody'):
            parent_node.finalbody.append(child_node)
        elif isinstance(parent_node, ast.Assert):
          if edge_type == 'test':
              parent_node.test = child_node
          elif edge_type == 'msg':
              parent_node.msg = child_node
        elif isinstance(parent_node, ast.Global) or isinstance(parent_node, ast.Nonlocal):
          pass
        elif isinstance(parent_node, ast.Pass) or isinstance(parent_node, ast.Break) or isinstance(parent_node, ast.Continue):
          pass
        elif isinstance(parent_node, ast.Await) or isinstance(parent_node, ast.Yield) or isinstance(parent_node, ast.YieldFrom):
          if edge_type == 'value':
            parent_node.value = child_node
        elif isinstance(parent_node, ast.Subscript):
          if edge_type == 'value':
              parent_node.value = child_node
          elif edge_type == 'slice':
              parent_node.slice = child_node
          elif edge_type == 'ctx':
              parent_node.ctx = child_node
        elif isinstance(parent_node, ast.Tuple):
          if edge_type.startswith('elts'):
              parent_node.elts.append(child_node)
          elif edge_type == 'ctx':
              parent_node.ctx = child_node
        elif isinstance(parent_node, ast.Slice):
          if edge_type == 'lower':
              parent_node.lower = child_node
          elif edge_type == 'upper':
              parent_node.upper = child_node
          elif edge_type == 'step':
              parent_node.step = child_node
        elif isinstance(parent_node, ast.Starred):
          if edge_type == 'value':
              parent_node.value = child_node
          elif edge_type == 'ctx':
              parent_node.ctx = child_node
        elif isinstance(parent_node, ast.keyword):
            if edge_type == 'value':
                parent_node.value = child_node
        
        
        else:
            raise ValueError(f"Invalid parent node type: {type(parent_node)}")

    # Fix missing locations in the AST
    ast.fix_missing_locations(ast_nodes[0])
    #return the ast tree representaion of the given tree 
    return ast_nodes[0]