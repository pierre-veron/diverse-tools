import numpy as np

def scatter_df(ax, df, x, y, color_by = None, marker_by = None, facecolor_by = None,
               listcolors = ['k', 'blue', 'purple', 'red'],
               listmarkers = ['o', 's', '^', '*'], 
               listfacecolors = ['same', 'w'], legend = True):
    """ Generate a scatter plot from a dataframe with different colors and/or
    markers and/or facecolors based on discrete values from specified columns. 

    Args:
        ax (matplotlib.Axes): plot to draw on
        df (pandas.Dataframe): data
        x (str): column name for the x data
        y (str): column name for the y data
        color_by (None or str, optional): Feature of the data for the coloring 
            of the points. If None, all points have same color, listcolors[0]. 
            Otherwise, must be a column name containing discrete values. 
            Defaults to None.
        marker_by (None or str, optional): Feature of the data for the marker style 
            of the points. If None, all points have same marker style, listmarkers[0]. 
            Otherwise, must be a column name containing discrete values. 
            Defaults to None.
        facecolor_by (None or str, optional): Feature of the data for the coloring 
            of the points face. If None, all points have same face color, 
            listfacecolors[0]. Otherwise, must be a column name containing discrete values. 
            Defaults to None.
        listcolors (list, optional): list of colors. Must contain at least the 
            number of different values of df[color_by] if specified. 
            Defaults to ['k', 'blue', 'purple', 'red'].
        listmarkers (list, optional): list of markers. Must contain at least the 
            number of different values of df[marker_by] if specified. 
            Defaults to ['o', 's', '^', '*'].
        listfacecolors (list, optional): list of colors. 'same' is accepted, in 
            this case the color is the same as the marker edge. Must contain at 
            least the number of different values of df[facecolor_by] if specified. 
            Defaults to ['same', 'w'].
        legend (bool, optional): add a legend. Defaults to True.
    """
    if marker_by is None:
        conditions_mark = [np.array([True]*len(df))]
        markers = [listmarkers[0]]
    else:
        set_mark = sorted(list(set(df[marker_by])))
        conditions_mark = []
        markers = []
        for i in range(len(set_mark)):
            conditions_mark.append(df[marker_by] == set_mark[i])
            markers.append(listmarkers[i])
            if legend:
                ax.plot([],[],ls="", marker = listmarkers[i], 
                        color = listcolors[0], label = "{}={}".format(marker_by,set_mark[i]))
    
    if color_by is None:
        conditions_col = [np.array([True]*len(df))]
        colors = listcolors[0]
    else:
        set_color = sorted(list(set(df[color_by])))
        conditions_col = []
        colors = []
        for i in range(len(set_color)):
            conditions_col.append(df[color_by] == set_color[i])
            colors.append(listcolors[i])
            if legend:
                ax.plot([],[],ls="",marker=listmarkers[0],color=listcolors[i],
                        label="{}={}".format(color_by,set_color[i]))
    
    if facecolor_by is None:
        conditions_fcol = [np.array([True]*len(df))]
        fcolors = [listfacecolors[0]]
    else:
        set_fcolor = sorted(list(set(df[facecolor_by])))
        conditions_fcol = []
        fcolors = []
        for i in range(len(set_fcolor)):
            conditions_fcol.append(df[facecolor_by] == set_fcolor[i])
            fcolors.append(listfacecolors[i])
            if legend:
                if listfacecolors[i]=="same":
                    fc=listcolors[0]
                else:
                    fc=listfacecolors[i]
                ax.plot([],[],ls="",marker=listmarkers[0],color=listcolors[0],
                        markerfacecolor=fc,label="{}={}".format(facecolor_by,set_fcolor[i]))
    for i_m in range(len(markers)):
        for i_c in range(len(colors)):
            for i_f in range(len(fcolors)):
                cond = (conditions_mark[i_m] & conditions_col[i_c]) & conditions_fcol[i_f]
                if listfacecolors[i_f] == "same":
                    fc = colors[i_c]
                else:
                    fc = listfacecolors[i_f]
                ax.plot(df.loc[cond, x], df.loc[cond, y], marker = markers[i_m], 
                        color = colors[i_c], ls = "", markerfacecolor = fc)
            

    if legend:
        ax.legend()
    ax.set_xlabel(x)
    ax.set_ylabel(y)