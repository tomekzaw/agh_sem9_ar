import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')

metrics = {
    'time': 'czasu wykonania',
    'speedup': 'przyspieszenia',
    'efficiency': 'efektywności'
}

ylabels = {
    'time': 'Czas wykonania [s]',
    'speedup': 'Przyspieszenie bezwzględne',
    'efficiency': 'Efektywność',
}


def assign_t1(df: pd.DataFrame) -> pd.DataFrame:
    df_t1 = df[df['np'] == 1].set_index('problem_size')['time'].groupby('problem_size').agg('mean').rename('t1')
    return df.merge(df_t1, on='problem_size')


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df['speedup'] = df['t1'] / df['time']
    df['efficiency'] = df['speedup'] / df['np']
    return df


def group_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(by=['problem_size', 'np', 'N', 'number_of_iterations'], dropna=False, as_index=False).agg({
        'time': ['count', 'mean', 'std'],
        'speedup': ['mean', 'std'],
        'efficiency': ['mean', 'std'],
    })


def plot(df: pd.DataFrame, metric: str) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 6))

    grouped = df.sort_values(by='problem_size').groupby('problem_size', dropna=False, sort=False)

    colors = ['red', 'green', 'blue']

    for (problem_size, group), color in zip(grouped, colors):
        ax.errorbar(x=group['np'],
                    y=group[metric, 'mean'],
                    yerr=group[metric, 'std'],
                    label=f'rozmiar problemu: {problem_size}',
                    color=color, fmt='.', ls='dotted', capsize=4)

    xs = [df['np'].min(), df['np'].max()]
    ys = xs if metric == 'speedup' else [1, 1] if metric == 'efficiency' else None
    if ys is not None:
        ax.plot(xs, ys, ls='dashed', lw=1, color='gray', label='przebieg idealny')

    ax.set(title=f'Zależność {metrics[metric]} od liczby procesów',
           xlabel='Liczba procesów',
           ylabel=ylabels[metric])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig.savefig(f'{metric}.png', bbox_inches='tight', dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    df = pd.read_csv('36_2.csv')
    df = assign_t1(df)
    df = calculate_metrics(df)
    df = group_data(df)

    plot(df, metric='speedup')
    plot(df, metric='efficiency')
