def demo_objgraph():
    x = []
    y = [x, [x], dict(x=x)]
    import objgraph
    objgraph.show_refs([y], filename='sample-graph.png')

    objgraph.show_most_common_types()


if __name__ == '__main__':
    demo_objgraph()
