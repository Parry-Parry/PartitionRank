
def load_monot5(checkpoint=None, batch_size : int = 64, **kwargs):
    from pyterrier_t5 import MonoT5ReRanker 

    return MonoT5ReRanker(model=checkpoint, batch_size=batch_size)

def load_bi_encoder(checkpoint=None, batch_size : int = 64, **kwargs):
    from transformers import AutoModel, AutoTokenizer
    from pyterrier_dr import HgfBiEncoder, BiScorer

    model = AutoModel.from_pretrained(checkpoint).cuda().eval()
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    backbone = HgfBiEncoder(model, tokenizer, {}, device=model.device)
    return BiScorer(backbone, batch_size=batch_size)

def load_splade(checkpoint=None, batch_size : int = 128, index : str = 'msmarco_passage', **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()
    from pyt_splade import SpladeFactory

    index = pt.IndexFactory.of(pt.get_dataset(index).get_index(), memory=True)
    splade = SpladeFactory(checkpoint)
    return splade.query_encoder(matchop=True, batch_size=batch_size) >> pt.BatchRetrieve(index, wmodel='Tf')

def load_bm25(index : str = 'msmarco_passage', **kwargs):
    import pyterrier as pt 
    if not pt.started(): pt.init()

    index = pt.IndexFactory.of(pt.get_dataset(index).get_index(), memory=True)
    return pt.BatchRetrieve(index, wmodel='BM25')

LOAD_FUNCS = {
    'monot5': load_monot5,
    'bi_encoder': load_bi_encoder,
    'splade': load_splade,
    'bm25': load_bm25
}